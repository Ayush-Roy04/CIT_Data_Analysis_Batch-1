import os
import sqlite3
import pandas as pd

# Configure pandas to show all columns without truncation in VS Code terminal
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

csv_filename = "UberCabFare_Cleaned.csv"
db_filename = "cab_fare.db"

# 1. Check if CSV file exists
if not os.path.exists(csv_filename):
  raise FileNotFoundError(
      f"'{csv_filename}' not found! Make sure the script is in the same folder as the CSV."
  )

# 2. Connect to SQLite database and load the table
conn = sqlite3.connect(db_filename)
df = pd.read_csv(csv_filename)
df.to_sql("rides", conn, index=False, if_exists="replace")
print(
    f"Loaded {len(df)} records into '{db_filename}' (table: 'rides') successfully.\n"
)


# 3. Execution helper function
def run_sql(query_title, query_string):
  print("=" * 80)
  print(f"QUERY: {query_title}")
  print("=" * 80)
  try:
    result_df = pd.read_sql_query(query_string, conn)
    print(result_df.to_string(index=False))
  except Exception as e:
    print(f"Error executing query: {e}")
  print("\n")


# ==========================================================
# ALL SQL QUERIES
# ==========================================================

# 1. Overall KPI Metrics (Matching Dashboard Cards)
run_sql(
    "1. Dashboard KPI Summary",
    """
SELECT 
    COUNT(*) AS total_rides,
    ROUND(SUM(final_fare), 2) AS total_revenue,
    ROUND(AVG(final_fare), 2) AS avg_fare,
    ROUND(SUM(distance_km), 2) AS total_distance_km,
    SUM(ride_requests) AS total_requests,
    ROUND(AVG(surge_multiplier), 2) AS avg_surge
FROM rides;
""",
)

# 2. Revenue and Volume by City
run_sql(
    "2. Revenue and Total Rides by City",
    """
SELECT 
    city,
    COUNT(*) AS total_rides,
    ROUND(SUM(final_fare), 2) AS total_revenue,
    ROUND(AVG(final_fare), 2) AS avg_fare,
    ROUND(AVG(distance_km), 2) AS avg_distance_km
FROM rides
GROUP BY city
ORDER BY total_revenue DESC;
""",
)

# 3. Vehicle Share and Percentage Contribution
run_sql(
    "3. Rides and Revenue by Vehicle Type",
    """
SELECT 
    type_of_vehicle,
    COUNT(*) AS ride_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rides), 2) AS share_percentage,
    ROUND(SUM(final_fare), 2) AS total_revenue,
    ROUND(AVG(final_fare), 2) AS avg_fare
FROM rides
GROUP BY type_of_vehicle
ORDER BY ride_count DESC;
""",
)

# 4. Traffic Level Impact on Fares, Duration, and Speed
run_sql(
    "4. Impact of Traffic Level on Speed and Fares",
    """
SELECT 
    traffic_level,
    COUNT(*) AS total_rides,
    ROUND(AVG(base_fare), 2) AS avg_base_fare,
    ROUND(AVG(final_fare), 2) AS avg_final_fare,
    ROUND(AVG(trip_duration), 2) AS avg_duration_mins,
    ROUND(AVG(distance_km / (trip_duration / 60.0)), 2) AS avg_speed_kmph
FROM rides
GROUP BY traffic_level
ORDER BY avg_final_fare DESC;
""",
)

# 5. Hourly Demand vs. Supply Profile (0 to 23 Hours)
run_sql(
    "5. Hourly Demand, Active Drivers, and Surge",
    """
SELECT 
    hour_of_day,
    SUM(ride_requests) AS total_requests,
    SUM(no_of_active_drivers) AS total_active_drivers,
    ROUND(AVG(demand_supply_ratio), 2) AS avg_demand_supply_ratio,
    ROUND(AVG(surge_multiplier), 2) AS avg_surge
FROM rides
GROUP BY hour_of_day
ORDER BY hour_of_day;
""",
)

# 6. Monthly Revenue Trend
run_sql(
    "6. Monthly Revenue and Ride Count Trend",
    """
SELECT 
    SUBSTR(ride_date, 1, 7) AS ride_month,
    COUNT(*) AS total_rides,
    ROUND(SUM(final_fare), 2) AS monthly_revenue,
    ROUND(AVG(final_fare), 2) AS avg_fare
FROM rides
GROUP BY ride_month
ORDER BY ride_month;
""",
)

# 7. City vs. Vehicle Matrix (Pivoted Average Fare)
run_sql(
    "7. Average Fare Matrix by City and Vehicle Type",
    """
SELECT 
    city,
    ROUND(AVG(CASE WHEN type_of_vehicle = 'Auto' THEN final_fare END), 2) AS auto,
    ROUND(AVG(CASE WHEN type_of_vehicle = 'Bike' THEN final_fare END), 2) AS bike,
    ROUND(AVG(CASE WHEN type_of_vehicle = 'Hatchback' THEN final_fare END), 2) AS hatchback,
    ROUND(AVG(CASE WHEN type_of_vehicle = 'Sedan' THEN final_fare END), 2) AS sedan,
    ROUND(AVG(CASE WHEN type_of_vehicle = 'Suv' THEN final_fare END), 2) AS suv,
    ROUND(AVG(final_fare), 2) AS city_total_avg
FROM rides
GROUP BY city
ORDER BY city_total_avg DESC;
""",
)

# 8. Weekday vs. Weekend Performance Comparison
run_sql(
    "8. Weekday vs. Weekend Performance",
    """
SELECT 
    CASE 
        WHEN day_of_week IN ('Saturday', 'Sunday') THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_rides,
    ROUND(SUM(final_fare), 2) AS total_revenue,
    ROUND(AVG(final_fare), 2) AS avg_fare,
    ROUND(AVG(surge_multiplier), 2) AS avg_surge
FROM rides
GROUP BY day_type;
""",
)

# 9. Pure Surge Revenue Contribution
run_sql(
    "9. Pure Surge Pricing Revenue Contribution",
    """
SELECT 
    ROUND(SUM(final_fare - base_fare), 2) AS total_surge_revenue,
    ROUND(AVG(final_fare - base_fare), 2) AS avg_surge_gain_per_ride,
    ROUND(SUM(final_fare - base_fare) * 100.0 / SUM(final_fare), 2) AS surge_contribution_pct
FROM rides;
""",
)

# 10. Top 3 Highest Earning Drivers per City (Window Function)
run_sql(
    "10. Top 3 Drivers per City (DENSE_RANK)",
    """
WITH RankedDrivers AS (
    SELECT 
        city,
        driver_name,
        ROUND(SUM(final_fare), 2) AS driver_revenue,
        DENSE_RANK() OVER (PARTITION BY city ORDER BY SUM(final_fare) DESC) AS rank_in_city
    FROM rides
    GROUP BY city, driver_name
)
SELECT city, driver_name, driver_revenue, rank_in_city
FROM RankedDrivers
WHERE rank_in_city <= 3
ORDER BY city, rank_in_city;
""",
)

# 11. Month-over-Month (MoM) Growth (Window Function LAG)
run_sql(
    "11. Month-over-Month (MoM) Revenue Growth Percentage",
    """
WITH MonthlyRevenue AS (
    SELECT 
        SUBSTR(ride_date, 1, 7) AS ride_month,
        ROUND(SUM(final_fare), 2) AS total_revenue
    FROM rides
    GROUP BY ride_month
)
SELECT 
    ride_month,
    total_revenue,
    LAG(total_revenue, 1) OVER (ORDER BY ride_month) AS previous_month_revenue,
    ROUND(
        ((total_revenue - LAG(total_revenue, 1) OVER (ORDER BY ride_month)) * 100.0) 
        / LAG(total_revenue, 1) OVER (ORDER BY ride_month), 
        2
    ) AS mom_growth_pct
FROM MonthlyRevenue
ORDER BY ride_month;
""",
)

# 12. Unmet Demand & Supply Deficit Hours
run_sql(
    "12. Top 5 Peak Hours with Highest Supply Deficit",
    """
SELECT 
    hour_of_day,
    SUM(ride_requests) AS total_requests,
    SUM(no_of_active_drivers) AS total_drivers,
    SUM(ride_requests) - SUM(no_of_active_drivers) AS unmet_capacity,
    ROUND(AVG(demand_supply_ratio), 2) AS avg_demand_supply_ratio
FROM rides
GROUP BY hour_of_day
ORDER BY unmet_capacity DESC
LIMIT 5;
""",
)

# 13. Trip Duration Brackets Analysis
run_sql(
    "13. Trip Duration Brackets (<30m, 30-60m, 61-90m, >90m)",
    """
SELECT 
    CASE 
        WHEN trip_duration < 30 THEN 'Under 30 Mins'
        WHEN trip_duration BETWEEN 30 AND 60 THEN '30-60 Mins'
        WHEN trip_duration BETWEEN 61 AND 90 THEN '61-90 Mins'
        ELSE 'Over 90 Mins'
    END AS duration_bracket,
    COUNT(*) AS total_rides,
    ROUND(AVG(distance_km), 2) AS avg_distance_km,
    ROUND(AVG(final_fare), 2) AS avg_fare,
    ROUND(SUM(final_fare), 2) AS total_revenue
FROM rides
GROUP BY duration_bracket
ORDER BY total_revenue DESC;
""",
)

# 14. Distance Tier Breakdown
run_sql(
    "14. Distance Tiers (Short, Medium, Long, Ultra Long)",
    """
SELECT 
    CASE 
        WHEN distance_km < 5 THEN 'Short (<5 km)'
        WHEN distance_km BETWEEN 5 AND 15 THEN 'Medium (5-15 km)'
        WHEN distance_km BETWEEN 15.01 AND 25 THEN 'Long (15-25 km)'
        ELSE 'Ultra Long (>25 km)'
    END AS distance_tier,
    COUNT(*) AS total_rides,
    ROUND(AVG(trip_duration), 2) AS avg_duration_mins,
    ROUND(AVG(final_fare), 2) AS avg_fare,
    ROUND(SUM(final_fare), 2) AS total_revenue
FROM rides
GROUP BY distance_tier
ORDER BY total_revenue DESC;
""",
)

# 15. Fleet Penetration Percentage per City
run_sql(
    "15. Vehicle Type Percentage Share within Each City",
    """
SELECT 
    city,
    type_of_vehicle,
    COUNT(*) AS rides_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY city), 2) AS pct_of_city_rides
FROM rides
GROUP BY city, type_of_vehicle
ORDER BY city, rides_count DESC;
""",
)

# 16. Multi-Trip Driver Performance
run_sql(
    "16. Driver Performance for Multi-Trip Drivers",
    """
SELECT 
    driver_name,
    city,
    COUNT(*) AS total_completed_rides,
    ROUND(SUM(final_fare), 2) AS total_fare_earned,
    ROUND(AVG(trip_duration), 2) AS avg_trip_duration,
    ROUND(AVG(distance_km), 2) AS avg_distance
FROM rides
GROUP BY driver_name, city
HAVING COUNT(*) > 1
ORDER BY total_fare_earned DESC
LIMIT 10;
""",
)

# 17. Extreme Congestion Outliers (Slowest Speeds < 10 km/h)
run_sql(
    "17. Extreme Congestion Rides (Speed < 10 km/h)",
    """
SELECT 
    user_id,
    city,
    type_of_vehicle,
    distance_km,
    trip_duration,
    traffic_level,
    ROUND(distance_km / (trip_duration / 60.0), 2) AS speed_kmph
FROM rides
WHERE (distance_km / (trip_duration / 60.0)) < 10.0
ORDER BY speed_kmph ASC
LIMIT 10;
""",
)

# 18. City Surge Frequency and Severity
run_sql(
    "18. Proportion of Surged Rides vs Regular Rides by City",
    """
SELECT 
    city,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN surge_multiplier > 1.0 THEN 1 ELSE 0 END) AS surged_rides,
    ROUND(SUM(CASE WHEN surge_multiplier > 1.0 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS surge_ride_pct,
    ROUND(AVG(surge_multiplier), 2) AS avg_surge_multiplier
FROM rides
GROUP BY city
ORDER BY surge_ride_pct DESC;
""",
)

# 19. Hourly Revenue Share Density
run_sql(
    "19. Hourly Revenue Contribution Percentage (Ranked by Revenue)",
    """
SELECT 
    hour_of_day,
    COUNT(*) AS rides_count,
    ROUND(SUM(final_fare), 2) AS hourly_revenue,
    ROUND(SUM(final_fare) * 100.0 / (SELECT SUM(final_fare) FROM rides), 2) AS revenue_pct_share
FROM rides
GROUP BY hour_of_day
ORDER BY hourly_revenue DESC
LIMIT 10;
""",
)

# 20. Statistical Fare Quartiles (NTILE Window Function)
run_sql(
    "20. Fare Quartiles (Q1 to Q4 Statistical Distribution)",
    """
WITH RankedFares AS (
    SELECT 
        user_id,
        city,
        final_fare,
        NTILE(4) OVER (ORDER BY final_fare) AS quartile
    FROM rides
)
SELECT 
    quartile,
    COUNT(*) AS total_rides,
    ROUND(MIN(final_fare), 2) AS min_fare,
    ROUND(MAX(final_fare), 2) AS max_fare,
    ROUND(AVG(final_fare), 2) AS avg_fare
FROM RankedFares
GROUP BY quartile;
""",
)

# 21. Traffic Level vs Vehicle Performance Matrix
run_sql(
    "21. Average Duration and Fare by Traffic Level & Vehicle Type",
    """
SELECT 
    traffic_level,
    type_of_vehicle,
    COUNT(*) AS total_rides,
    ROUND(AVG(trip_duration), 2) AS avg_duration_mins,
    ROUND(AVG(final_fare), 2) AS avg_fare
FROM rides
GROUP BY traffic_level, type_of_vehicle
ORDER BY traffic_level, total_rides DESC;
""",
)

# 22. Top Extreme Surge Incidents
run_sql(
    "22. Rides with Extreme Surge Multipliers (>= 1.8x)",
    """
SELECT 
    user_id,
    city,
    hour_of_day,
    day_of_week,
    type_of_vehicle,
    traffic_level,
    demand_supply_ratio,
    surge_multiplier,
    final_fare
FROM rides
WHERE surge_multiplier >= 1.8
ORDER BY surge_multiplier DESC, final_fare DESC
LIMIT 10;
""",
)

# 23. Busiest Single Hour for Every Day of the Week
run_sql(
    "23. Busiest Peak Hour for Each Day of the Week",
    """
WITH DailyHourlyAgg AS (
    SELECT 
        day_of_week,
        hour_of_day,
        COUNT(*) AS ride_count,
        ROW_NUMBER() OVER (PARTITION BY day_of_week ORDER BY COUNT(*) DESC) AS rnk
    FROM rides
    GROUP BY day_of_week, hour_of_day
)
SELECT 
    day_of_week, 
    hour_of_day AS peak_hour, 
    ride_count AS max_rides
FROM DailyHourlyAgg
WHERE rnk = 1
ORDER BY max_rides DESC;
""",
)

# 24. Base Fare vs Surge Premium Breakdown by Vehicle Type
run_sql(
    "24. Base Fare vs Pure Surge Markup by Vehicle Type",
    """
SELECT 
    type_of_vehicle,
    ROUND(AVG(base_fare), 2) AS avg_base_fare,
    ROUND(AVG(final_fare), 2) AS avg_final_fare,
    ROUND(AVG(final_fare - base_fare), 2) AS avg_surge_premium,
    ROUND(AVG((final_fare - base_fare) * 100.0 / final_fare), 2) AS surge_pct_of_fare
FROM rides
GROUP BY type_of_vehicle
ORDER BY avg_surge_premium DESC;
""",
)
# 25. Fare Volatility & Spread by City
run_sql(
    "25. Fare Spread and Variance Across Cities",
    """
SELECT 
    city,
    ROUND(MIN(final_fare), 2) AS min_fare,
    ROUND(MAX(final_fare), 2) AS max_fare,
    ROUND(MAX(final_fare) - MIN(final_fare), 2) AS fare_spread,
    ROUND(AVG(final_fare), 2) AS avg_fare,
    ROUND(AVG(final_fare * final_fare) - AVG(final_fare) * AVG(final_fare), 2) AS fare_variance
FROM rides
GROUP BY city
ORDER BY fare_spread DESC;
""",
)

# 26. Weekend vs Weekday Revenue Contribution per City
run_sql(
    "26. Weekend Revenue Percentage by City",
    """
SELECT 
    city,
    ROUND(SUM(CASE WHEN day_of_week IN ('Saturday', 'Sunday') THEN final_fare ELSE 0 END), 2) AS weekend_revenue,
    ROUND(SUM(CASE WHEN day_of_week NOT IN ('Saturday', 'Sunday') THEN final_fare ELSE 0 END), 2) AS weekday_revenue,
    ROUND(
        SUM(CASE WHEN day_of_week IN ('Saturday', 'Sunday') THEN final_fare ELSE 0 END) * 100.0 / SUM(final_fare), 
        2
    ) AS weekend_rev_pct
FROM rides
GROUP BY city
ORDER BY weekend_rev_pct DESC;
""",
)

# 27. Vehicle Preference by Day of the Week
run_sql(
    "27. Vehicle Type Demand Breakdown by Day of Week (Top Combinations)",
    """
SELECT 
    day_of_week,
    type_of_vehicle,
    COUNT(*) AS rides_count,
    ROUND(SUM(final_fare), 2) AS total_revenue
FROM rides
GROUP BY day_of_week, type_of_vehicle
ORDER BY rides_count DESC
LIMIT 12;
""",
)

# 28. Surge Multiplier Sensitivity to Traffic Levels
run_sql(
    "28. Average Surge Multiplier and Demand-Supply Ratio by Traffic Level",
    """
SELECT 
    traffic_level,
    COUNT(*) AS ride_count,
    ROUND(AVG(surge_multiplier), 2) AS avg_surge_multiplier,
    ROUND(AVG(demand_supply_ratio), 2) AS avg_demand_supply_ratio
FROM rides
GROUP BY traffic_level
ORDER BY avg_surge_multiplier DESC;
""",
)

# 29. Top 5% Highest Fares (Percentile Ranking using PERCENT_RANK)
run_sql(
    "29. Outlier Trips: Top 5th Percentile Fares (95th+ Percentile)",
    """
WITH RankedTrips AS (
    SELECT 
        user_id,
        city,
        type_of_vehicle,
        distance_km,
        trip_duration,
        surge_multiplier,
        final_fare,
        PERCENT_RANK() OVER (ORDER BY final_fare) AS pct_rank
    FROM rides
)
SELECT 
    user_id,
    city,
    type_of_vehicle,
    distance_km,
    trip_duration,
    surge_multiplier,
    final_fare,
    ROUND(pct_rank * 100.0, 2) AS percentile
FROM RankedTrips
WHERE pct_rank >= 0.95
ORDER BY final_fare DESC
LIMIT 10;
""",
)

# 30. Congestion Frequency: Busiest Hours for Jam & High Traffic
run_sql(
    "30. Peak Congestion Hours (High Traffic and Jams)",
    """
SELECT 
    hour_of_day,
    traffic_level,
    COUNT(*) AS incident_count,
    ROUND(AVG(trip_duration), 2) AS avg_duration_mins
FROM rides
WHERE traffic_level IN ('Jam', 'High')
GROUP BY hour_of_day, traffic_level
ORDER BY incident_count DESC
LIMIT 10;
""",
)

# 31. Weighted Unit Pricing (True Total Fare / Total Distance per City)
run_sql(
    "31. Weighted City Revenue Rate (Total Fare / Total Kilometers)",
    """
SELECT 
    city,
    ROUND(SUM(final_fare), 2) AS total_revenue,
    ROUND(SUM(distance_km), 2) AS total_km_driven,
    ROUND(SUM(final_fare) / SUM(distance_km), 2) AS weighted_fare_per_km,
    ROUND(AVG(trip_duration), 2) AS avg_trip_mins
FROM rides
GROUP BY city
ORDER BY weighted_fare_per_km DESC;
""",
)

# 32. Drivers Outperforming Their City Benchmark
run_sql(
    "32. Drivers Earning Significantly Above City Average",
    """
WITH DriverEarnings AS (
    SELECT 
        city,
        driver_name,
        COUNT(*) AS trips,
        AVG(final_fare) AS avg_driver_fare
    FROM rides
    GROUP BY city, driver_name
),
CityBenchmarks AS (
    SELECT 
        city,
        AVG(final_fare) AS city_avg_fare
    FROM rides
    GROUP BY city
)
SELECT 
    d.driver_name,
    d.city,
    d.trips,
    ROUND(d.avg_driver_fare, 2) AS driver_avg_fare,
    ROUND(c.city_avg_fare, 2) AS city_avg_fare,
    ROUND(d.avg_driver_fare - c.city_avg_fare, 2) AS fare_premium
FROM DriverEarnings d
JOIN CityBenchmarks c ON d.city = c.city
WHERE d.avg_driver_fare > c.city_avg_fare
ORDER BY fare_premium DESC
LIMIT 10;
""",
)

# 33. Revenue Productivity by Hour Tiers (NTILE 3)
run_sql(
    "33. Hour Productivity Tiers (High, Medium, Low Yielding Hours)",
    """
WITH HourlyTiers AS (
    SELECT 
        hour_of_day,
        SUM(final_fare) AS total_rev,
        NTILE(3) OVER (ORDER BY SUM(final_fare) DESC) AS tier
    FROM rides
    GROUP BY hour_of_day
)
SELECT 
    CASE 
        WHEN tier = 1 THEN 'Tier 1: Peak Revenue Hours'
        WHEN tier = 2 THEN 'Tier 2: Mid-tier Hours'
        ELSE 'Tier 3: Low Revenue Hours'
    END AS hour_tier,
    COUNT(hour_of_day) AS number_of_hours,
    ROUND(SUM(total_rev), 2) AS tier_revenue,
    ROUND(AVG(total_rev), 2) AS avg_rev_per_hour
FROM HourlyTiers
GROUP BY tier;
""",
)

# 34. Fare Elasticity: Ratio of Surge Revenue to Base Revenue per Vehicle
run_sql(
    "34. Surge Multiplier Lift Ratio by Vehicle Type",
    """
SELECT 
    type_of_vehicle,
    ROUND(SUM(base_fare), 2) AS total_base_revenue,
    ROUND(SUM(final_fare), 2) AS total_realized_revenue,
    ROUND(SUM(final_fare - base_fare), 2) AS surge_gain,
    ROUND((SUM(final_fare) / SUM(base_fare)), 2) AS aggregate_surge_multiplier
FROM rides
GROUP BY type_of_vehicle
ORDER BY aggregate_surge_multiplier DESC;
""",
)

# Close connection
conn.close()
print("All SQL queries executed successfully.")
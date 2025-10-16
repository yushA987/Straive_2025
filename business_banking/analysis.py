import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv('logs.csv')

# Parse timestamp with explicit format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S,%f')

# Extract UserID if available
df['UserID'] = df['Message'].str.extract(r"User '?(\w+)'?")

# Summary stats
print("=== Log Level Counts ===")
print(df['Level'].value_counts())
print()

print("=== Total Logs:", len(df))
print("=== Unique Users (from logs):", df['UserID'].nunique())
print()

# Most active users
print("=== Top 5 Active Users ===")
print(df['UserID'].value_counts().head())
print()

# Last activity per user
print("=== Last Activity Timestamp per User ===")
print(df.groupby('UserID')['Timestamp'].max().dropna().sort_values(ascending=False))
print()

# Separate warnings and errors
warnings_df = df[df['Level'] == 'WARNING']
errors_df = df[df['Level'] == 'ERROR']

print("=== Warning Count:", len(warnings_df))
print("=== Error Count:", len(errors_df))
print()

# Top warning messages
print("=== Top Warning Messages ===")
print(warnings_df['Message'].value_counts().head(5))
print()

# Set timestamp index for resampling
df.set_index('Timestamp', inplace=True)
logs_per_hour = df.resample('h').size()

print("=== Logs Per Hour ===")
print(logs_per_hour.tail())
print()

# Plot: Logs per hour
plt.figure(figsize=(12, 6))
logs_per_hour.plot(title='Log Entries Per Hour', grid=True)
plt.xlabel('Time')
plt.ylabel('Number of Logs')
plt.tight_layout()
plt.savefig('log_frequency_per_hour.png')
plt.close()

# Plot: Warnings per hour
# Must set index for resampling
warnings_df = warnings_df.set_index('Timestamp')
plt.figure(figsize=(12, 6))
warnings_df.resample('h').size().plot(color='orange', title='Warnings Per Hour', grid=True)
plt.xlabel('Time')
plt.ylabel('Number of Warnings')
plt.tight_layout()
plt.savefig('warnings_per_hour.png')
plt.close()

# Detect unauthorized access
unauthorized_access = df[df['Message'].str.contains('Unauthorized access attempt', case=False, na=False)]
print("=== Unauthorized Access Attempts ===")
print(unauthorized_access[['UserID', 'Message']].tail(10))
print()

# Token issues (unauthorized, expired, invalid)
token_issues = df[df['Message'].str.contains('token', case=False, na=False)]
print("=== Token-related Issues ===")
print(token_issues[['UserID', 'Message']].tail(10))
print()

# Save filtered data to CSVs (optional)
warnings_df.reset_index().to_csv('warnings.csv', index=False)
unauthorized_access.reset_index().to_csv('failed_access_attempts.csv', index=False)
token_issues.reset_index().to_csv('token_issues.csv', index=False)

print("✅ Analysis complete. Plots saved:")
print(" - log_frequency_per_hour.png")
print(" - warnings_per_hour.png")

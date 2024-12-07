# Dictionary mapping function names to code snippets
unique_code_snippets = {
    "fraud_detection": """def fraud_detection():
    print("Executing: Fraud Detection")
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Step 1: Load the dataset
def load_data():
    # Replace with the path to your dataset
    data = pd.read_csv('creditcard.csv')
    return data

# Step 2: Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())
    
    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Class distribution
    sns.countplot(x='Class', data=data)
    plt.title('Class Distribution (0: Non-Fraud, 1: Fraud)')
    plt.show()

    # Correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.show()

# Step 3: Preprocess the Data
def preprocess_data(data):
    # Standardizing 'Amount' and other features
    scaler = StandardScaler()
    data[['Amount']] = scaler.fit_transform(data[['Amount']])
    data_scaled = data.drop('Time', axis=1)  # Drop the 'Time' column
    
    return data_scaled

# Step 4: Split the Data
def split_data(data_scaled):
    X = data_scaled.drop('Class', axis=1)
    y = data_scaled['Class']
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

# Step 5: Train the Random Forest Model
def train_random_forest(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Step 6: Evaluate the Model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    # Print classification report
    print("Classification Report (Random Forest):")
    print(classification_report(y_test, y_pred))

    # Print confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix (Random Forest):")
    print(conf_matrix)

    # Accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nAccuracy: {accuracy * 100:.2f}%')

    # Visualize confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Fraud', 'Fraud'], yticklabels=['Non-Fraud', 'Fraud'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# Step 7: Optional Anomaly Detection using Isolation Forest
def anomaly_detection(X_test, y_test):
    model_iforest = IsolationForest(contamination=0.01, random_state=42)
    y_pred_iforest = model_iforest.fit_predict(X_test)

    # Convert predictions to 0 or 1 (fraud or non-fraud)
    y_pred_iforest = [1 if i == -1 else 0 for i in y_pred_iforest]

    # Evaluate the anomaly detection model
    print("Classification Report (Isolation Forest):")
    print(classification_report(y_test, y_pred_iforest))

    # Confusion Matrix for Isolation Forest
    conf_matrix_iforest = confusion_matrix(y_test, y_pred_iforest)
    print("Confusion Matrix (Isolation Forest):")
    print(conf_matrix_iforest)

    # Visualize confusion matrix for Isolation Forest
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix_iforest, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Fraud', 'Fraud'], yticklabels=['Non-Fraud', 'Fraud'])
    plt.title('Confusion Matrix (Isolation Forest)')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# Main function to run the analysis
def main():
    # Step 1: Load the dataset
    data = load_data()

    # Step 2: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 3: Preprocess the data
    data_scaled = preprocess_data(data)

    # Step 4: Split the data into training and test sets
    X_train, X_test, y_train, y_test = split_data(data_scaled)

    # Step 5: Train the Random Forest model
    model = train_random_forest(X_train, y_train)

    # Step 6: Evaluate the Random Forest model
    evaluate_model(model, X_test, y_test)

    # Step 7: Optional Anomaly Detection using Isolation Forest
    anomaly_detection(X_test, y_test)

if __name__ == '__main__':
    main()
""",
    
    "sales_forecasting": """def sales_forecasting():
    print("Executing: Sales Forecasting")
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Load the dataset (replace with the path to your file)
def load_data():
    data = pd.read_csv('store_sales.csv', parse_dates=['date'], index_col='date')
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())
    
    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Plot total sales over time
    plt.figure(figsize=(10, 6))
    plt.plot(data['sales'])
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.show()

# Step 2: Preprocess Data
def preprocess_data(data):
    # Fill missing values (if any) using forward fill method
    data.fillna(method='ffill', inplace=True)

    # Resample the data to daily frequency and aggregate sales
    daily_data = data.resample('D').sum()

    return daily_data

# Step 3: Decompose the Time Series
def decompose_data(daily_data):
    decomposition = seasonal_decompose(daily_data['sales'], model='multiplicative', period=365)
    decomposition.plot()
    plt.show()

# Step 4: Feature Engineering (Add Day of the Week, Month, and Holiday Features)
def add_features(daily_data):
    daily_data['day_of_week'] = daily_data.index.dayofweek
    daily_data['month'] = daily_data.index.month
    daily_data['is_holiday'] = daily_data.index.isin(pd.to_datetime(['2024-12-25', '2024-01-01']))  # Example holidays

    return daily_data

# Step 5: Train-Test Split
def train_test_split_data(daily_data):
    X = daily_data[['day_of_week', 'month', 'is_holiday']]
    y = daily_data['sales']
    
    # Split data into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    return X_train, X_test, y_train, y_test

# Step 6: Train the Model
def train_model(X_train, y_train):
    # Using Linear Regression as a simple model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model

# Step 7: Evaluate the Model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Mean Absolute Error (MAE): {mae:.2f}')

    # Plot actual vs predicted sales
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test, label='Actual Sales')
    plt.plot(y_test.index, y_pred, label='Predicted Sales', linestyle='--')
    plt.title('Actual vs Predicted Sales')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

# Step 8: Forecast Future Sales
def forecast_sales(model, X_test):
    # Forecast sales for the next 30 days
    future_dates = pd.date_range(start=X_test.index[-1], periods=31, freq='D')
    future_X = pd.DataFrame({
        'day_of_week': future_dates.dayofweek,
        'month': future_dates.month,
        'is_holiday': future_dates.isin(pd.to_datetime(['2024-12-25', '2024-01-01']))  # Example holidays
    })
    
    future_sales = model.predict(future_X)
    
    # Plot future forecast
    plt.figure(figsize=(10, 6))
    plt.plot(future_dates, future_sales, label='Forecasted Sales', color='orange')
    plt.title('Sales Forecast for Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

# Main function to run the analysis
def main():
    # Load and preprocess the data
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess Data
    daily_data = preprocess_data(data)

    # Step 3: Decompose the Time Series
    decompose_data(daily_data)

    # Step 4: Add additional features for forecasting
    daily_data = add_features(daily_data)

    # Step 5: Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split_data(daily_data)

    # Step 6: Train the model
    model = train_model(X_train, y_train)

    # Step 7: Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Step 8: Forecast future sales for the next 30 days
    forecast_sales(model, X_test)

if __name__ == '__main__':
    main()
""",
    
    "customer_segmentation": """def customer_segmentation():
    print("Executing: Customer Segmentation")
   # customer_segmentation.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Load the dataset (replace with the path to your file)
def load_data():
    data = pd.read_csv('customer_segmentation.csv')
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())
    
    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())
    
    # Visualize distributions of some key features
    sns.histplot(data['Age'], kde=True)
    plt.title('Age Distribution')
    plt.show()

    sns.histplot(data['Annual Income (k$)'], kde=True)
    plt.title('Annual Income Distribution')
    plt.show()

# Step 2: Preprocess Data (Handling missing values, scaling, etc.)
def preprocess_data(data):
    # Fill missing values with the mean of the respective column
    data.fillna(data.mean(), inplace=True)

    # Selecting only numerical columns for clustering (assuming demographic and behavioral data)
    data_numerical = data[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]

    # Scaling the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_numerical)

    return data_scaled

# Step 3: Apply K-Means Clustering
def apply_kmeans_clustering(data_scaled):
    # Choosing the optimal number of clusters using the Elbow method
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
        kmeans.fit(data_scaled)
        wcss.append(kmeans.inertia_)

    # Plotting the Elbow graph
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 11), wcss)
    plt.title('Elbow Method for Optimal Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS (Within-cluster sum of squares)')
    plt.show()

    # From the elbow plot, select the optimal number of clusters (for this example, assume 5)
    optimal_clusters = 5
    kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(data_scaled)

    return kmeans

# Step 4: Analyze and Visualize Customer Segments
def visualize_segments(data_scaled, kmeans):
    # Assigning cluster labels to the original data
    data['Cluster'] = kmeans.labels_

    # Visualize the clusters in 2D using PCA for dimensionality reduction
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data_scaled)
    pca_df = pd.DataFrame(data=principal_components, columns=['PCA1', 'PCA2'])
    pca_df['Cluster'] = kmeans.labels_

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=pca_df, palette='viridis', s=100, alpha=0.7)
    plt.title('Customer Segments')
    plt.show()

# Step 5: Evaluate the Clustering Performance
def evaluate_clustering(kmeans, data_scaled):
    silhouette_avg = silhouette_score(data_scaled, kmeans.labels_)
    print(f'Silhouette Score: {silhouette_avg:.2f}')

# Main function to run the analysis
def main():
    # Load the data
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data_scaled = preprocess_data(data)

    # Step 3: Apply K-Means Clustering
    kmeans = apply_kmeans_clustering(data_scaled)

    # Step 4: Visualize the customer segments
    visualize_segments(data_scaled, kmeans)

    # Step 5: Evaluate the clustering performance
    evaluate_clustering(kmeans, data_scaled)

if __name__ == '__main__':
    main()
""",
    
    "efficiency_optimization": """def efficiency_optimization():
    print("Executing: Efficiency Optimization")
   # transportation_efficiency.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Load the dataset (replace with the path to your file)
def load_data():
    data = pd.read_csv('traffic_transport.csv', parse_dates=['timestamp'])
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())
    
    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())
    
    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())
    
    # Plot delay distribution
    sns.histplot(data['delay'], kde=True)
    plt.title('Delay Distribution')
    plt.xlabel('Delay (minutes)')
    plt.ylabel('Frequency')
    plt.show()

# Step 2: Preprocess the Data (Handling missing values, feature extraction)
def preprocess_data(data):
    # Fill missing values (if any) with the median of the column
    data['delay'].fillna(data['delay'].median(), inplace=True)
    
    # Extract useful features: Hour of the day, Day of the week, etc.
    data['hour'] = data['timestamp'].dt.hour
    data['day_of_week'] = data['timestamp'].dt.dayofweek
    data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    return data

# Step 3: Analyze Delays by Route and Hour of the Day
def analyze_delays_by_route_and_hour(data):
    # Average delay by route
    route_delays = data.groupby('route')['delay'].mean().sort_values(ascending=False)
    print("\nAverage Delay by Route:")
    print(route_delays)
    
    # Plot average delay by route
    route_delays.plot(kind='bar', figsize=(10, 6))
    plt.title('Average Delay by Route')
    plt.xlabel('Route')
    plt.ylabel('Average Delay (minutes)')
    plt.show()

    # Average delay by hour of the day
    hour_delays = data.groupby('hour')['delay'].mean()
    print("\nAverage Delay by Hour:")
    print(hour_delays)
    
    # Plot average delay by hour
    hour_delays.plot(kind='line', figsize=(10, 6))
    plt.title('Average Delay by Hour of the Day')
    plt.xlabel('Hour')
    plt.ylabel('Average Delay (minutes)')
    plt.show()

# Step 4: Identify Clusters of Delays (Using K-Means)
def identify_clusters(data):
    # Prepare the data for clustering
    data_cluster = data[['delay', 'hour', 'day_of_week', 'is_weekend']]
    
    # Normalize the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_cluster)
    
    # Use K-Means to identify clusters
    kmeans = KMeans(n_clusters=3, random_state=42)
    data['cluster'] = kmeans.fit_predict(data_scaled)
    
    # Plot clusters based on delay and hour
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hour', y='delay', hue='cluster', data=data, palette='viridis', s=100, alpha=0.7)
    plt.title('Clusters of Delays by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Delay (minutes)')
    plt.show()

    # Print Silhouette Score to evaluate clustering performance
    silhouette_avg = silhouette_score(data_scaled, data['cluster'])
    print(f'\nSilhouette Score for Clustering: {silhouette_avg:.2f}')

# Step 5: Identify Inefficiencies and Propose Improvements
def identify_inefficiencies(data):
    # Routes with high delays
    high_delay_routes = data.groupby('route')['delay'].mean().sort_values(ascending=False).head(5)
    print("\nRoutes with the Highest Average Delays:")
    print(high_delay_routes)

    # Peak hours with high delays
    peak_hours = data.groupby('hour')['delay'].mean().sort_values(ascending=False).head(5)
    print("\nPeak Hours with the Highest Average Delays:")
    print(peak_hours)

    # Weekends with high delays
    weekend_delays = data[data['is_weekend'] == 1].groupby('hour')['delay'].mean().sort_values(ascending=False)
    print("\nWeekend Hours with High Delays:")
    print(weekend_delays.head(5))

# Main function to run the analysis
def main():
    # Load the data
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Analyze delays by route and hour of the day
    analyze_delays_by_route_and_hour(data)

    # Step 4: Identify clusters of delays
    identify_clusters(data)

    # Step 5: Identify inefficiencies and propose improvements
    identify_inefficiencies(data)

if __name__ == '__main__':
    main()
""",

    "student_performance_analysis": """def student_performance_analysis():
    print("Executing: Student Performance Analysis")
    # student_performance_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Load the dataset (replace with the path to your file)
def load_data():
    data = pd.read_csv('student_performance.csv')
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())
    
    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())
    
    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())
    
    # Visualize distribution of grades
    sns.histplot(data['G3'], kde=True, color='blue')
    plt.title('Distribution of Final Grades')
    plt.xlabel('Grade')
    plt.ylabel('Frequency')
    plt.show()

# Step 2: Correlation Analysis to Identify Significant Factors
def correlation_analysis(data):
    # Correlation matrix
    correlation_matrix = data.corr()
    
    # Plot heatmap of correlations
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()
    
    print("\nCorrelation between features:")
    print(correlation_matrix)

# Step 3: Preprocess the Data (Handle missing values, encoding categorical variables)
def preprocess_data(data):
    # Fill missing values (if any) with median
    data.fillna(data.median(), inplace=True)

    # Encoding categorical variables (convert strings to numbers)
    data = pd.get_dummies(data, drop_first=True)
    
    return data

# Step 4: Train a model to predict student performance (G3 - final grade)
def train_model(data):
    # Define the feature columns (all columns except the target column 'G3')
    X = data.drop(columns=['G3'])
    
    # Define the target variable (final grade 'G3')
    y = data['G3']
    
    # Split the dataset into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Instantiate the Linear Regression model
    model = LinearRegression()
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model performance
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R2) Score: {r2:.2f}")
    
    # Visualize Actual vs Predicted values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, color='blue')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.title('Actual vs Predicted Grades')
    plt.xlabel('Actual Grades')
    plt.ylabel('Predicted Grades')
    plt.show()

    return model, X_test, y_test, y_pred

# Step 5: Identify Key Factors Influencing Performance
def identify_key_factors(model, X_test, y_test):
    # Get the feature coefficients from the trained model
    feature_coefficients = model.coef_

    # Create a DataFrame for the coefficients
    feature_importance = pd.DataFrame({
        'Feature': X_test.columns,
        'Coefficient': feature_coefficients
    })

    # Sort by absolute value of coefficients
    feature_importance['Importance'] = feature_importance['Coefficient'].abs()
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False)

    print("\nKey Features Influencing Student Performance (Sorted by Importance):")
    print(feature_importance[['Feature', 'Importance']])

# Step 6: Propose Potential Interventions
def propose_interventions(data):
    # Analyzing high-impact features based on the correlation matrix and feature importance
    # Focus on factors that can be improved, e.g., attendance, study time, socio-economic status
    
    print("\nProposed Interventions to Improve Student Performance:")
    print("- Encourage students with low study time to increase their study hours.")
    print("- Improve attendance rates through incentive programs or addressing absenteeism causes.")
    print("- Target socio-economic support for students who are financially disadvantaged.")
    print("- Offer tutoring or additional academic support for students with lower grades.")
    print("- Increase parental involvement for students from households with low education levels.")

# Main function to run the analysis
def main():
    # Load the data
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Correlation analysis to identify significant factors
    correlation_analysis(data)

    # Step 3: Preprocess the data
    data = preprocess_data(data)

    # Step 4: Train a model to predict student performance
    model, X_test, y_test, y_pred = train_model(data)

    # Step 5: Identify key factors influencing performance
    identify_key_factors(model, X_test, y_test)

    # Step 6: Propose potential interventions
    propose_interventions(data)

if __name__ == '__main__':
    main()
""",

    "credit_scoring": """def credit_scoring():
    print("Executing: Credit Scoring")
    # credit_scoring.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve

# Load the dataset (replace with the path to your file)
def load_data():
    data = pd.read_csv('loan_prediction.csv')
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())
    
    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())
    
    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize target variable distribution (Loan Status)
    sns.countplot(x='Loan_Status', data=data)
    plt.title('Loan Default Status Distribution')
    plt.show()

# Preprocess the Data (Handle missing values, encoding categorical variables)
def preprocess_data(data):
    # Fill missing values for numerical columns
    data.fillna(data.median(), inplace=True)
    
    # Handle missing categorical values (e.g., filling with mode)
    data['Gender'].fillna(data['Gender'].mode()[0], inplace=True)
    data['Dependents'].fillna(data['Dependents'].mode()[0], inplace=True)
    data['Marital_Status'].fillna(data['Marital_Status'].mode()[0], inplace=True)
    data['Self_Employed'].fillna(data['Self_Employed'].mode()[0], inplace=True)
    data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].mode()[0], inplace=True)
    data['Credit_History'].fillna(data['Credit_History'].mode()[0], inplace=True)
    
    # Encoding categorical variables using Label Encoding
    label_encoder = LabelEncoder()
    data['Gender'] = label_encoder.fit_transform(data['Gender'])
    data['Marital_Status'] = label_encoder.fit_transform(data['Marital_Status'])
    data['Self_Employed'] = label_encoder.fit_transform(data['Self_Employed'])
    data['Loan_Status'] = label_encoder.fit_transform(data['Loan_Status'])
    data['Education'] = label_encoder.fit_transform(data['Education'])
    data['Property_Area'] = label_encoder.fit_transform(data['Property_Area'])
    
    return data

# Train the model to predict loan default
def train_model(data):
    # Define feature columns (all columns except target 'Loan_Status')
    X = data.drop(columns=['Loan_Status'])
    
    # Define the target variable (loan default status)
    y = data['Loan_Status']
    
    # Split the dataset into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Instantiate the Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    
    # Confusion Matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Default', 'Default'], yticklabels=['No Default', 'Default'])
    plt.title('Confusion Matrix')
    plt.show()

    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # ROC Curve and AUC
    y_prob = model.predict_proba(X_test)[:, 1]  # Probability of the positive class
    roc_auc = roc_auc_score(y_test, y_prob)
    print(f"\nROC AUC Score: {roc_auc:.4f}")

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', label=f'ROC curve (area = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.show()

    return model, X_test, y_test, y_pred

# Main function to run the analysis
def main():
    # Load the dataset
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Train the model to predict loan default
    model, X_test, y_test, y_pred = train_model(data)

if __name__ == '__main__':
    main()
""",

    "price_prediction": """def price_prediction():
    print("Executing: Price Prediction")
    # housing_price_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load the dataset
def load_data():
    data = pd.read_csv('housing_prices.csv')  # Replace with your dataset path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize the distribution of house prices
    plt.figure(figsize=(10, 6))
    sns.histplot(data['SalePrice'], kde=True, bins=30)
    plt.title('Distribution of House Prices')
    plt.xlabel('SalePrice')
    plt.ylabel('Frequency')
    plt.show()

    # Correlation heatmap to identify significant features
    correlation = data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()

# Preprocess the Data (Handle missing values, encoding categorical variables)
def preprocess_data(data):
    # Handle missing values by filling numerical columns with the median and categorical columns with the mode
    data.fillna(data.median(), inplace=True)
    for col in data.select_dtypes(include=['object']).columns:
        data[col].fillna(data[col].mode()[0], inplace=True)

    # Encoding categorical variables using Label Encoding
    label_encoder = LabelEncoder()
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = label_encoder.fit_transform(data[col])

    return data

# Train the regression model to predict house prices
def train_model(data):
    # Define features and target variable
    X = data.drop(columns=['SalePrice'])  # All features except the target variable
    y = data['SalePrice']  # Target variable: SalePrice

    # Split the data into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Instantiate the Linear Regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model's performance
    print(f"Model Performance:")
    print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
    print(f"R-squared Score: {r2_score(y_test, y_pred):.4f}")

    # Plot Actual vs Predicted Prices
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color='blue', alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
    plt.title('Actual vs Predicted House Prices')
    plt.xlabel('Actual Prices')
    plt.ylabel('Predicted Prices')
    plt.show()

    return model, X_test, y_test, y_pred

# Main function to run the analysis
def main():
    # Load the dataset
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Train the model to predict house prices
    model, X_test, y_test, y_pred = train_model(data)

if __name__ == '__main__':
    main()
""",

    "crop_yield_prediction": """def crop_yield_prediction():
    print("Executing: Crop Yield Prediction")
    # crop_yield_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load the dataset
def load_data():
    data = pd.read_csv('crop_yield_data.csv')  # Replace with your dataset path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize the distribution of crop yield
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Yield'], kde=True, bins=30)
    plt.title('Distribution of Crop Yield')
    plt.xlabel('Crop Yield')
    plt.ylabel('Frequency')
    plt.show()

    # Correlation heatmap to identify significant features
    correlation = data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()

# Preprocess the Data (Handle missing values, encoding categorical variables)
def preprocess_data(data):
    # Handle missing values by filling numerical columns with the median and categorical columns with the mode
    data.fillna(data.median(), inplace=True)
    for col in data.select_dtypes(include=['object']).columns:
        data[col].fillna(data[col].mode()[0], inplace=True)

    # Encoding categorical variables using Label Encoding
    label_encoder = LabelEncoder()
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = label_encoder.fit_transform(data[col])

    return data

# Train the regression model to predict crop yield
def train_model(data):
    # Define features and target variable
    X = data.drop(columns=['Yield'])  # All features except the target variable
    y = data['Yield']  # Target variable: Crop Yield

    # Split the data into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Instantiate the Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model's performance
    print(f"Model Performance:")
    print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"Root Mean Squared Error: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
    print(f"R-squared Score: {r2_score(y_test, y_pred):.4f}")

    # Feature importance (which features are most important in predicting crop yield)
    feature_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    feature_importance.plot(kind='bar')
    plt.title('Feature Importance')
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.show()

    # Plot Actual vs Predicted Crop Yield
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color='blue', alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
    plt.title('Actual vs Predicted Crop Yield')
    plt.xlabel('Actual Yield')
    plt.ylabel('Predicted Yield')
    plt.show()

    return model, X_test, y_test, y_pred

# Main function to run the analysis
def main():
    # Load the dataset
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Train the model to predict crop yield
    model, X_test, y_test, y_pred = train_model(data)

if __name__ == '__main__':
    main()
""",

    "air_quality_analysis": """def air_quality_analysis():
    print("Executing: Air Quality Analysis")
   # air_quality_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the dataset
def load_data():
    data = pd.read_csv('air_quality_data.csv')  # Replace with your dataset path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize pollutant distributions
    pollutants = ['PM2.5', 'CO', 'NO2', 'SO2']
    data[pollutants].hist(bins=30, figsize=(10, 6))
    plt.suptitle('Pollutant Distributions')
    plt.show()

    # Correlation matrix to identify relationships between pollutants
    plt.figure(figsize=(10, 8))
    correlation_matrix = data[pollutants].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Pollutant Correlation Heatmap')
    plt.show()

# Handle missing values and preprocess the data
def preprocess_data(data):
    # Fill missing values with the median for numerical columns
    data.fillna(data.median(), inplace=True)
    return data

# Perform clustering to identify pollution hotspots
def clustering(data):
    # Select relevant pollutants for clustering
    pollutants = ['PM2.5', 'CO', 'NO2', 'SO2']
    
    # Normalize the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[pollutants])

    # Apply KMeans clustering to find hotspots
    kmeans = KMeans(n_clusters=3, random_state=42)  # Using 3 clusters (change as needed)
    data['Cluster'] = kmeans.fit_predict(data_scaled)

    # Visualize the clusters
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data['PM2.5'], y=data['NO2'], hue=data['Cluster'], palette='viridis', s=100)
    plt.title('Pollution Hotspots (PM2.5 vs NO2)')
    plt.xlabel('PM2.5')
    plt.ylabel('NO2')
    plt.show()

    return kmeans, data

# Apply PCA for dimensionality reduction and visualize
def apply_pca(data):
    pollutants = ['PM2.5', 'CO', 'NO2', 'SO2']
    
    # Standardize the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[pollutants])
    
    # Apply PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data_scaled)
    
    # Create a DataFrame for PCA results
    pca_df = pd.DataFrame(pca_result, columns=['PCA1', 'PCA2'])
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(pca_df['PCA1'], pca_df['PCA2'], c=data['Cluster'], cmap='viridis', s=100)
    plt.title('PCA of Air Quality Data')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.show()

# Analyze the factors contributing to pollution
def analyze_factors(data):
    # Calculate the correlation between pollutants and other factors like city (if available)
    city_pollutants = data.groupby('City')[['PM2.5', 'CO', 'NO2', 'SO2']].mean()
    
    # Visualize the average pollution levels by city
    city_pollutants.plot(kind='bar', figsize=(12, 8))
    plt.title('Average Pollutant Levels by City')
    plt.ylabel('Concentration (µg/m³ or ppm)')
    plt.show()

# Main function to run the analysis
def main():
    # Load the dataset
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Clustering to identify pollution hotspots
    kmeans, data_with_clusters = clustering(data)

    # Step 4: Apply PCA for dimensionality reduction and visualization
    apply_pca(data_with_clusters)

    # Step 5: Analyze the factors contributing to pollution
    analyze_factors(data_with_clusters)

if __name__ == '__main__':
    main()
""",

    "player_performance_analysis": """def player_performance_analysis():
    print("Executing: Player Performance Analysis")
    # player_performance_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data():
    data = pd.read_csv('nba_player_stats.csv')  # Replace with your dataset path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize key statistics distributions
    metrics = ['Points', 'Assists', 'Rebounds', 'Steals', 'Blocks']
    data[metrics].hist(bins=30, figsize=(12, 8))
    plt.suptitle('Distributions of Key Player Metrics')
    plt.show()

    # Correlation matrix to identify relationships between metrics
    plt.figure(figsize=(10, 8))
    correlation_matrix = data[metrics].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of Player Metrics')
    plt.show()

# Handle missing values and preprocess the data
def preprocess_data(data):
    # Fill missing values with the median for numerical columns
    data.fillna(data.median(), inplace=True)
    return data

# Feature selection and regression model to predict player performance
def predict_performance(data):
    # Feature selection
    features = ['Assists', 'Rebounds', 'Steals', 'Blocks']  # Example features, you can add more
    target = 'Points'  # Target variable: points scored

    # Prepare the feature and target datasets
    X = data[features]
    y = data[target]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply Linear Regression model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Predict on test data
    y_pred = model.predict(X_test_scaled)

    # Evaluate the model performance
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Visualize the predictions vs actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title('Actual vs Predicted Points')
    plt.xlabel('Actual Points')
    plt.ylabel('Predicted Points')
    plt.show()

    return model

# Analyze the importance of features in predicting performance
def feature_importance(model, data):
    # Coefficients of the linear regression model
    features = ['Assists', 'Rebounds', 'Steals', 'Blocks']
    importance = model.coef_

    # Display the importance of each feature
    feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    print("\nFeature Importance (based on coefficients):")
    print(feature_importance_df)

# Predict the performance of a new player
def predict_new_player_performance(model, new_player_data):
    # Assuming new_player_data is a DataFrame with the same features (Assists, Rebounds, Steals, Blocks)
    prediction = model.predict(new_player_data)
    print("\nPredicted Points for New Player:", prediction[0])

# Main function to run the analysis
def main():
    # Load the dataset
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Build the regression model to predict player performance
    model = predict_performance(data)

    # Step 4: Analyze feature importance
    feature_importance(model, data)

    # Step 5: Predict the performance of a new player (example)
    new_player_data = pd.DataFrame({
        'Assists': [5],
        'Rebounds': [7],
        'Steals': [2],
        'Blocks': [1]
    })
    predict_new_player_performance(model, new_player_data)

if __name__ == '__main__':
    main()
""",

    "prediction_modeling": """def prediction_modeling():
    print("Executing: Prediction Modeling")
    # weather_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data():
    data = pd.read_csv('weather_data.csv')  # Replace with your dataset path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize key statistics distributions
    data[['Temperature', 'Humidity', 'Precipitation']].hist(bins=30, figsize=(12, 8))
    plt.suptitle('Distributions of Weather Metrics')
    plt.show()

    # Correlation matrix to identify relationships between metrics
    plt.figure(figsize=(8, 6))
    correlation_matrix = data[['Temperature', 'Humidity', 'Precipitation']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of Weather Metrics')
    plt.show()

# Handle missing values and preprocess the data
def preprocess_data(data):
    # Fill missing values with the median for numerical columns
    data.fillna(data.median(), inplace=True)
    return data

# Feature selection and regression model for predicting weather (e.g., Temperature)
def predict_weather(data):
    # Feature selection: Let's predict Temperature using Humidity and Precipitation
    features = ['Humidity', 'Precipitation']  # Example features for predicting Temperature
    target = 'Temperature'  # Target variable: Temperature

    # Prepare the feature and target datasets
    X = data[features]
    y = data[target]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply Random Forest model (more robust than linear regression for complex data)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Predict on test data
    y_pred = model.predict(X_test_scaled)

    # Evaluate the model performance
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Visualize the predictions vs actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title('Actual vs Predicted Temperature')
    plt.xlabel('Actual Temperature')
    plt.ylabel('Predicted Temperature')
    plt.show()

    return model

# Predict weather for new data
def predict_new_weather(model, new_data):
    # Assuming new_data is a DataFrame with the same features (Humidity, Precipitation)
    prediction = model.predict(new_data)
    print("\nPredicted Temperature for New Data:", prediction[0])

# Main function to run the analysis
def main():
    # Load the dataset
    data = load_data()

    # Step 1: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 2: Preprocess the data
    data = preprocess_data(data)

    # Step 3: Build the weather prediction model
    model = predict_weather(data)

    # Step 4: Predict the temperature for new data (example)
    new_data = pd.DataFrame({
        'Humidity': [75],
        'Precipitation': [0.12]
    })
    predict_new_weather(model, new_data)

if __name__ == '__main__':
    main()
""",

    "customer_churn_prediction": """def customer_churn_prediction():
    print("Executing: Customer Churn Prediction")
   # churn_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the dataset
def load_data():
    data = pd.read_csv('Telco-Customer-Churn.csv')  # Replace with your file path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize churn distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Churn', data=data)
    plt.title('Churn Distribution')
    plt.show()

# Preprocess data: Convert categorical features and handle missing data
def preprocess_data(data):
    # Handle missing values
    data.fillna(method='ffill', inplace=True)

    # Convert categorical columns to numeric using LabelEncoder
    le = LabelEncoder()
    data['gender'] = le.fit_transform(data['gender'])
    data['Partner'] = le.fit_transform(data['Partner'])
    data['Dependents'] = le.fit_transform(data['Dependents'])
    data['PhoneService'] = le.fit_transform(data['PhoneService'])
    data['MultipleLines'] = le.fit_transform(data['MultipleLines'])
    data['InternetService'] = le.fit_transform(data['InternetService'])
    data['OnlineSecurity'] = le.fit_transform(data['OnlineSecurity'])
    data['OnlineBackup'] = le.fit_transform(data['OnlineBackup'])
    data['DeviceProtection'] = le.fit_transform(data['DeviceProtection'])
    data['TechSupport'] = le.fit_transform(data['TechSupport'])
    data['StreamingTV'] = le.fit_transform(data['StreamingTV'])
    data['StreamingMovies'] = le.fit_transform(data['StreamingMovies'])
    data['Contract'] = le.fit_transform(data['Contract'])
    data['PaperlessBilling'] = le.fit_transform(data['PaperlessBilling'])
    data['PaymentMethod'] = le.fit_transform(data['PaymentMethod'])
    data['Churn'] = le.fit_transform(data['Churn'])

    return data

# Feature selection and splitting data
def split_data(data):
    features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 
                'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
                'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']
    X = data[features]
    y = data['Churn']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scaling features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test

# Build and train the Random Forest model
def build_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Visualizing the Confusion Matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', linewidths=0.5)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# Main function to execute the steps
def main():
    # Step 1: Load the dataset
    data = load_data()

    # Step 2: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 3: Preprocess the data
    data = preprocess_data(data)

    # Step 4: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(data)

    # Step 5: Build the model
    model = build_model(X_train, y_train)

    # Step 6: Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "consumption_optimization": """def consumption_optimization():
    print("Executing: Consumption Optimization")
    ## energy_consumption_optimization.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data():
    data = pd.read_csv('household_energy_consumption.csv')  # Replace with your file path
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Basic statistical summary
    print("\nBasic Statistical Summary:")
    print(data.describe())

    # Visualize consumption patterns
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Time', y='EnergyConsumption', data=data)
    plt.title('Energy Consumption Over Time')
    plt.xlabel('Time')
    plt.ylabel('Energy Consumption')
    plt.show()

# Preprocess data: Convert time to datetime and handle missing values
def preprocess_data(data):
    # Convert time to datetime if it's not in datetime format
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    
    # Handle missing values by forward filling
    data.fillna(method='ffill', inplace=True)

    # Extract additional time features like hour, day, etc.
    data['Hour'] = data['Time'].dt.hour
    data['Day'] = data['Time'].dt.dayofweek

    return data

# Feature selection and splitting data
def split_data(data):
    features = ['Temperature', 'Occupancy', 'Hour', 'Day']
    X = data[features]
    y = data['EnergyConsumption']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scaling features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test

# Build and train the Random Forest model
def build_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Hyperparameter tuning using GridSearchCV
def tune_model(X_train, y_train):
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_search = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R2 Score:", r2_score(y_test, y_pred))

    # Visualize the predictions
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test, label='Actual Energy Consumption', color='blue')
    plt.plot(y_test.index, y_pred, label='Predicted Energy Consumption', color='red')
    plt.title('Actual vs Predicted Energy Consumption')
    plt.xlabel('Time')
    plt.ylabel('Energy Consumption')
    plt.legend()
    plt.show()

# Main function to execute the steps
def main():
    # Step 1: Load the dataset
    data = load_data()

    # Step 2: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 3: Preprocess the data
    data = preprocess_data(data)

    # Step 4: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(data)

    # Step 5: Build the model
    model = build_model(X_train, y_train)

    # Optionally, use GridSearchCV for hyperparameter tuning
    # model = tune_model(X_train, y_train)

    # Step 6: Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "sentiment_analysis": """def sentiment_analysis():
    print("Executing: Sentiment Analysis")
    # sentiment_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

# Load the dataset
def load_data():
    # Replace 'twitter_sentiment.csv' with the path to your dataset
    data = pd.read_csv('twitter_sentiment.csv')
    return data

# Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    print("Dataset Information:")
    print(data.info())
    print("\nFirst few rows of the dataset:")
    print(data.head())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Visualize the sentiment distribution
    sns.countplot(x='sentiment', data=data)
    plt.title('Distribution of Sentiments')
    plt.show()

# Preprocess the data: Clean the text and handle labels
def preprocess_data(data):
    # Drop any rows with missing labels or text
    data.dropna(subset=['text', 'sentiment'], inplace=True)
    
    # Clean text (remove special characters, URLs, etc.)
    data['text'] = data['text'].str.replace(r'http\S+', '', regex=True)  # Remove URLs
    data['text'] = data['text'].str.replace(r'@\w+', '', regex=True)  # Remove mentions
    data['text'] = data['text'].str.replace(r'[^a-zA-Z\s]', '', regex=True)  # Remove non-alphabetical chars
    data['text'] = data['text'].str.lower()  # Convert to lowercase

    return data

# Feature extraction and splitting data
def split_data(data):
    X = data['text']  # Features: the tweet text
    y = data['sentiment']  # Labels: the sentiment (positive, negative, neutral)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

# Build and train the Naive Bayes model
def build_model(X_train, y_train):
    # Using a pipeline with TF-IDF Vectorizer and Naive Bayes classifier
    pipeline = make_pipeline(TfidfVectorizer(), MultinomialNB())
    pipeline.fit(X_train, y_train)
    return pipeline

# Hyperparameter tuning (optional)
def tune_model(X_train, y_train):
    param_grid = {
        'tfidfvectorizer__max_df': [0.75, 1.0],
        'tfidfvectorizer__min_df': [1, 2],
        'multinomialnb__alpha': [0.5, 1.0, 1.5]
    }
    grid_search = GridSearchCV(make_pipeline(TfidfVectorizer(), MultinomialNB()), param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print("Accuracy Score:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Confusion matrix plot
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# Main function to execute the steps
def main():
    # Step 1: Load the dataset
    data = load_data()

    # Step 2: Perform Exploratory Data Analysis (EDA)
    perform_eda(data)

    # Step 3: Preprocess the data
    data = preprocess_data(data)

    # Step 4: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(data)

    # Step 5: Build the model
    model = build_model(X_train, y_train)

    # Optionally, tune the model using GridSearchCV
    # model = tune_model(X_train, y_train)

    # Step 6: Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "delivery_optimization": """def delivery_optimization():
    print("Executing: Delivery Optimization")
    # delivery_optimization.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

# Step 1: Load and inspect the dataset
def load_data():
    # Replace 'delivery_data.csv' with the actual path to your dataset
    data = pd.read_csv('delivery_data.csv')
    print(data.head())
    return data

# Step 2: Route optimization using TSP (Traveling Salesman Problem)
def route_optimization(locations):
    # Locations should be a dataframe with 'latitude' and 'longitude' of delivery points
    distance_matrix = cdist(locations[['latitude', 'longitude']], locations[['latitude', 'longitude']], metric='euclidean')

    # Solving TSP using linear sum assignment (Hungarian method)
    row_ind, col_ind = linear_sum_assignment(distance_matrix)

    # Optimized route order
    optimized_route = locations.iloc[col_ind]
    return optimized_route

# Step 3: Predict delivery times using a machine learning model (Linear Regression)
def predict_delivery_time(data):
    # Assuming 'product_weight', 'route_distance' are features and 'delivery_time' is the target variable
    X = data[['product_weight', 'route_distance']]  # Features
    y = data['delivery_time']  # Target variable (delivery time)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test_scaled)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    return model, scaler

# Step 4: Visualize route optimization
def visualize_route(optimized_route):
    plt.figure(figsize=(10, 6))
    plt.scatter(optimized_route['longitude'], optimized_route['latitude'], c='blue', label='Delivery Points')
    plt.plot(optimized_route['longitude'], optimized_route['latitude'], c='red', label='Optimized Route')
    plt.title('Optimized Delivery Route')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

# Step 5: Main function to run the steps
def main():
    # Step 1: Load data
    data = load_data()

    # Step 2: Route optimization (assuming 'latitude' and 'longitude' are columns for locations)
    locations = data[['latitude', 'longitude']]  # Replace with your specific columns for delivery points
    optimized_route = route_optimization(locations)

    # Step 3: Predict delivery times based on features
    model, scaler = predict_delivery_time(data)

    # Step 4: Visualize the optimized route
    visualize_route(optimized_route)

if __name__ == '__main__':
    main()
""",

    "destination_popularity_analysis": """def destination_popularity_analysis():
    print("Executing: Destination Popularity Analysis")
   # tourism_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Step 1: Load and inspect the dataset
def load_data():
    # Replace 'tourism_data.csv' with the actual path to your dataset
    data = pd.read_csv('tourism_data.csv')
    print(data.head())
    print(data.describe())
    return data

# Step 2: Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Summary statistics and null value check
    print("Missing values:", data.isnull().sum())
    
    # Visualizing distributions of key columns
    plt.figure(figsize=(10, 6))
    sns.histplot(data['rating'], kde=True, bins=30)
    plt.title('Distribution of Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.show()
    
    # Correlation matrix
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()

# Step 3: Clustering destinations based on rating and number of attractions
def cluster_destinations(data):
    # Use columns like 'rating' and 'num_attractions' for clustering (adjust according to your dataset)
    features = data[['rating', 'num_attractions']]  # Assuming these columns exist
    
    # Handle missing values
    features.fillna(features.mean(), inplace=True)
    
    # Standardize the data
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=5, random_state=42)  # You can experiment with the number of clusters
    data['cluster'] = kmeans.fit_predict(features_scaled)

    return data, kmeans

# Step 4: Visualize the clustering results
def visualize_clusters(data):
    # Reduce to 2D using PCA for visualization purposes
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(data[['rating', 'num_attractions']])
    data['pca1'], data['pca2'] = pca_components[:, 0], pca_components[:, 1]
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=data, palette='viridis')
    plt.title('Tourist Destinations Clusters')
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.show()

# Step 5: Main function to run the analysis
def main():
    # Step 1: Load data
    data = load_data()

    # Step 2: Perform EDA
    perform_eda(data)

    # Step 3: Cluster the destinations
    clustered_data, kmeans_model = cluster_destinations(data)

    # Step 4: Visualize clustering results
    visualize_clusters(clustered_data)

    # Optional: Show cluster centers (centroids) in the scaled feature space
    print("Cluster Centers (Centroids):\n", kmeans_model.cluster_centers_)

if __name__ == '__main__':
    main()
""",

    "vehicle_price_prediction": """def vehicle_price_prediction():
    print("Executing: Vehicle Price Prediction")
    # car_price_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load and inspect the dataset
def load_data():
    # Replace 'car_price_data.csv' with the actual path to your dataset
    data = pd.read_csv('car_price_data.csv')
    print(data.head())
    print(data.describe())
    print(data.info())
    return data

# Step 2: Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Check for missing values
    print("Missing values:\n", data.isnull().sum())
    
    # Visualize price distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data['price'], kde=True, bins=30)
    plt.title('Distribution of Vehicle Prices')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.show()
    
    # Visualize correlations between numerical features
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()

# Step 3: Feature Engineering (Handling categorical variables)
def preprocess_data(data):
    # Convert 'make' and 'model' to categorical variables using one-hot encoding
    data = pd.get_dummies(data, drop_first=True)
    
    # Handle missing values (e.g., fill with median)
    data.fillna(data.median(), inplace=True)
    
    # Separate features and target variable
    X = data.drop(columns=['price'])
    y = data['price']
    
    # Standardize numerical features (optional)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# Step 4: Train a Regression Model (Random Forest Regressor)
def train_model(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model (Random Forest Regressor)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, X_test, y_test

# Step 5: Evaluate the Model
def evaluate_model(model, X_test, y_test):
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate the performance metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-squared: {r2}")
    
    # Plot the actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linewidth=2)
    plt.title('Actual vs Predicted Prices')
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.show()

# Step 6: Main function to run the analysis
def main():
    # Step 1: Load data
    data = load_data()

    # Step 2: Perform EDA
    perform_eda(data)

    # Step 3: Preprocess the data
    X, y = preprocess_data(data)

    # Step 4: Train the model
    model, X_test, y_test = train_model(X, y)

    # Step 5: Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "popularity_analysis": """def popularity_analysis():
    print("Executing: Popularity Analysis")
    # movie_popularity_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Step 1: Load and inspect the dataset
def load_data():
    # Replace 'movies.csv' with the actual path to your dataset
    data = pd.read_csv('movies.csv')
    print(data.head())
    print(data.describe())
    print(data.info())
    return data

# Step 2: Perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Check for missing values
    print("Missing values:\n", data.isnull().sum())
    
    # Visualize distribution of ratings
    plt.figure(figsize=(10, 6))
    sns.histplot(data['rating'], kde=True, bins=30)
    plt.title('Distribution of Movie Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.show()
    
    # Visualize the distribution of release years
    plt.figure(figsize=(10, 6))
    sns.histplot(data['release_year'], kde=False, bins=30)
    plt.title('Distribution of Movie Release Years')
    plt.xlabel('Release Year')
    plt.ylabel('Frequency')
    plt.show()

# Step 3: Feature Engineering for Recommendation System
def preprocess_data(data):
    # Handle missing values in 'genres' and 'description' columns
    data['genres'] = data['genres'].fillna('')
    data['description'] = data['description'].fillna('')
    
    # Combine relevant features into one text field for content-based recommendation
    data['content'] = data['genres'] + ' ' + data['description']
    
    return data

# Step 4: Build Content-Based Recommendation System
def build_recommendation_system(data):
    # Vectorize the 'content' column using TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['content'])
    
    # Calculate cosine similarity between movies
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return cosine_sim

# Step 5: Generate Recommendations for a Given Movie
def recommend_movies(movie_title, data, cosine_sim):
    # Find the index of the movie that matches the title
    idx = data[data['title'] == movie_title].index[0]
    
    # Get the pairwise similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices of the top 10 most similar movies
    top_similar_movies = sim_scores[1:11]
    
    # Get movie titles of the top 10 similar movies
    movie_indices = [i[0] for i in top_similar_movies]
    recommended_movies = data['title'].iloc[movie_indices]
    
    return recommended_movies

# Step 6: Analyze Factors Contributing to Popularity
def analyze_popularity(data):
    # Visualize the correlation between different factors
    plt.figure(figsize=(10, 6))
    sns.heatmap(data[['rating', 'release_year', 'vote_count']].corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation between Ratings, Release Year, and Vote Count')
    plt.show()
    
    # Investigate how rating and vote count affect popularity
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='rating', y='vote_count', data=data)
    plt.title('Rating vs Vote Count')
    plt.xlabel('Rating')
    plt.ylabel('Vote Count')
    plt.show()

# Step 7: Main function to run the analysis and build recommendation system
def main():
    # Step 1: Load the data
    data = load_data()
    
    # Step 2: Perform EDA
    perform_eda(data)
    
    # Step 3: Preprocess the data
    data = preprocess_data(data)
    
    # Step 4: Build the recommendation system
    cosine_sim = build_recommendation_system(data)
    
    # Step 5: Recommend movies for a given title
    movie_title = 'The Dark Knight'  # Change this to any movie title from the dataset
    recommended_movies = recommend_movies(movie_title, data, cosine_sim)
    print(f"Top 10 recommended movies similar to {movie_title}:\n", recommended_movies)
    
    # Step 6: Analyze factors contributing to popularity
    analyze_popularity(data)

if __name__ == '__main__':
    main()
""",

    "customer_feedback_analysis": """def customer_feedback_analysis():
    print("Executing: Customer Feedback Analysis")
    # customer_feedback_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
from collections import Counter
import re

# Step 1: Load and inspect the dataset
def load_data():
    # Replace 'yelp_reviews.csv' with the actual path to your Yelp reviews dataset
    data = pd.read_csv('yelp_reviews.csv')
    print(data.head())
    print(data.describe())
    print(data.info())
    return data

# Step 2: Clean and preprocess the text data
def preprocess_data(data):
    # Remove missing values in the 'text' column
    data = data.dropna(subset=['text'])
    
    # Clean the text (remove special characters, convert to lowercase)
    data['cleaned_text'] = data['text'].apply(lambda x: re.sub(r'[^A-Za-z0-9\s]', '', x.lower()))
    
    return data

# Step 3: Perform Sentiment Analysis to gauge customer satisfaction
def sentiment_analysis(data):
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    
    # Apply sentiment analysis
    data['sentiment'] = data['cleaned_text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Classify as positive, negative, or neutral based on sentiment score
    data['sentiment_label'] = data['sentiment'].apply(lambda x: 'positive' if x > 0.1 else ('negative' if x < -0.1 else 'neutral'))
    
    # Visualize the sentiment distribution
    plt.figure(figsize=(8, 6))
    sns.countplot(x='sentiment_label', data=data, palette='Set2')
    plt.title('Sentiment Distribution of Reviews')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()
    
    return data

# Step 4: Identify the most frequent words/complaints using Word Cloud
def word_frequency_analysis(data):
    stop_words = set(stopwords.words('english'))
    
    # Combine all the reviews into one text block
    text = " ".join(review for review in data['cleaned_text'])
    
    # Generate word cloud for complaints
    wordcloud = WordCloud(stopwords=stop_words, background_color='white', width=800, height=400).generate(text)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Cloud for Customer Reviews')
    plt.axis('off')
    plt.show()
    
    # Most common words in the reviews (excluding stop words)
    vectorizer = CountVectorizer(stop_words=stop_words, max_features=20)
    X = vectorizer.fit_transform(data['cleaned_text'])
    word_count = np.array(X.sum(axis=0)).flatten()
    words = vectorizer.get_feature_names_out()
    
    # Create a DataFrame for top words
    word_freq = pd.DataFrame(list(zip(words, word_count)), columns=['Word', 'Frequency'])
    word_freq = word_freq.sort_values(by='Frequency', ascending=False)
    
    print("Most Frequent Words in Reviews:\n", word_freq.head(10))
    
    return word_freq

# Step 5: Propose Improvements Based on Feedback
def propose_improvements(word_freq, data):
    # Analyze frequent complaints and compliments based on top words
    complaints = word_freq[word_freq['Frequency'] > 10]['Word'].tolist()  # Threshold based on frequency
    compliments = ['good', 'excellent', 'great', 'amazing', 'awesome', 'best']
    
    # Propose improvements
    complaints_str = ", ".join(complaints)
    print(f"Common Complaints Based on Word Frequency Analysis: {complaints_str}")
    
    # Compliment Analysis - identify compliment reviews
    compliment_reviews = data[data['cleaned_text'].apply(lambda x: any(word in x for word in compliments))]
    print(f"Proposed Improvements for Restaurant Services:")
    print("1. Focus on improving service in areas related to common complaints such as:", complaints_str)
    print("2. Maintain the positive aspects of the service, such as:", ", ".join(compliments))
    
    print(f"\nTotal Compliment Reviews: {len(compliment_reviews)}")
    print(f"Total Complaint Reviews: {len(data) - len(compliment_reviews)}")

# Step 6: Main function to run the analysis
def main():
    # Step 1: Load the data
    data = load_data()
    
    # Step 2: Preprocess the data
    data = preprocess_data(data)
    
    # Step 3: Perform Sentiment Analysis
    data = sentiment_analysis(data)
    
    # Step 4: Word Frequency Analysis
    word_freq = word_frequency_analysis(data)
    
    # Step 5: Propose improvements based on feedback
    propose_improvements(word_freq, data)

if __name__ == '__main__':
    main()
""",

    "quality_control": """def quality_control():
    print("Executing: Quality Control")
    # manufacturing_quality_control.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import regularizers

# Step 1: Load and inspect the dataset
def load_data():
    # Load dataset (replace 'manufacturing_data.csv' with your actual file)
    data = pd.read_csv('manufacturing_data.csv')
    print("First 5 rows of the dataset:")
    print(data.head())
    print("\nDataset Info:")
    print(data.info())
    print("\nDataset Description:")
    print(data.describe())
    return data

# Step 2: Data Preprocessing
def preprocess_data(data):
    # Drop any rows with missing values (if necessary)
    data = data.dropna()

    # Check for any duplicate entries
    data = data.drop_duplicates()

    # Standardize the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    return data_scaled

# Step 3: Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Visualize the distribution of the data
    plt.figure(figsize=(10, 6))
    sns.histplot(data, kde=True)
    plt.title("Distribution of Sensor Data")
    plt.xlabel("Sensor Measurement")
    plt.ylabel("Frequency")
    plt.show()

    # Correlation matrix
    corr = np.corrcoef(data, rowvar=False)
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    plt.show()

# Step 4: Anomaly Detection using Statistical Methods
def statistical_anomaly_detection(data):
    # Calculate Z-scores
    from scipy.stats import zscore
    z_scores = np.abs(zscore(data))
    anomalies_zscore = np.where(z_scores > 3)  # Threshold for anomalies (z > 3)
    
    print(f"Anomalies detected based on Z-Score method: {len(anomalies_zscore[0])}")
    return anomalies_zscore

# Step 5: Anomaly Detection using Machine Learning Models
def machine_learning_anomaly_detection(data):
    # Use Isolation Forest for anomaly detection
    iso_forest = IsolationForest(contamination=0.05)  # 5% contamination expected
    anomalies_if = iso_forest.fit_predict(data)
    anomalies_if = np.where(anomalies_if == -1)

    # Use One-Class SVM for anomaly detection
    one_class_svm = OneClassSVM(nu=0.05, kernel="rbf", gamma='scale')
    anomalies_svm = one_class_svm.fit_predict(data)
    anomalies_svm = np.where(anomalies_svm == -1)

    print(f"Anomalies detected using Isolation Forest: {len(anomalies_if[0])}")
    print(f"Anomalies detected using One-Class SVM: {len(anomalies_svm[0])}")
    
    return anomalies_if, anomalies_svm

# Step 6: Anomaly Detection using Autoencoders (Deep Learning)
def deep_learning_anomaly_detection(data):
    # Autoencoder Model
    input_dim = data.shape[1]
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(input_dim, activation='sigmoid'))

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(data, data, epochs=20, batch_size=256, validation_data=(data, data), verbose=1)

    # Predict reconstruction error
    reconstructed_data = model.predict(data)
    reconstruction_error = np.mean(np.square(data - reconstructed_data), axis=1)

    # Define a threshold for anomaly detection (95th percentile)
    threshold = np.percentile(reconstruction_error, 95)
    anomalies_autoencoder = np.where(reconstruction_error > threshold)

    print(f"Anomalies detected using Autoencoder: {len(anomalies_autoencoder[0])}")
    
    return anomalies_autoencoder

# Step 7: Visualize Anomalies
def visualize_anomalies(data, anomalies, title="Anomalies Detected"):
    plt.figure(figsize=(10, 6))
    plt.scatter(np.arange(len(data)), data[:, 0], c='blue', label='Normal')
    plt.scatter(anomalies[0], data[anomalies[0], 0], c='red', label='Anomalies')
    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Sensor Data")
    plt.legend()
    plt.show()

# Step 8: Main Function to Run Analysis
def main():
    # Step 1: Load the dataset
    data = load_data()

    # Step 2: Preprocess the data
    data_scaled = preprocess_data(data)

    # Step 3: Perform EDA
    perform_eda(data_scaled)

    # Step 4: Statistical Anomaly Detection
    anomalies_zscore = statistical_anomaly_detection(data_scaled)

    # Step 5: Machine Learning Anomaly Detection
    anomalies_if, anomalies_svm = machine_learning_anomaly_detection(data_scaled)

    # Step 6: Deep Learning Anomaly Detection (Autoencoder)
    anomalies_autoencoder = deep_learning_anomaly_detection(data_scaled)

    # Step 7: Visualize anomalies detected
    visualize_anomalies(data_scaled, anomalies_zscore, title="Anomalies Detected with Z-Score")
    visualize_anomalies(data_scaled, anomalies_if, title="Anomalies Detected with Isolation Forest")
    visualize_anomalies(data_scaled, anomalies_svm, title="Anomalies Detected with One-Class SVM")
    visualize_anomalies(data_scaled, anomalies_autoencoder, title="Anomalies Detected with Autoencoder")

if __name__ == '__main__':
    main()
""",

    "claims_prediction": """def claims_prediction():
    print("Executing: Claims Prediction")
    # insurance_claims_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Step 1: Load and Inspect the Data
def load_data():
    # Load the dataset (replace 'insurance_claims.csv' with your actual file)
    data = pd.read_csv('insurance_claims.csv')
    print("First 5 rows of the dataset:")
    print(data.head())
    print("\nDataset Info:")
    print(data.info())
    print("\nDataset Description:")
    print(data.describe())
    return data

# Step 2: Data Preprocessing
def preprocess_data(data):
    # Handle missing values (if any)
    data = data.dropna()  # Drop rows with missing values (or use imputation if required)

    # Convert categorical variables to numerical using Label Encoding or One-Hot Encoding
    label_encoder = LabelEncoder()
    if 'target' in data.columns:
        data['target'] = label_encoder.fit_transform(data['target'])
    
    # Convert other categorical columns if present (e.g., policy type, region)
    # data['policy_type'] = label_encoder.fit_transform(data['policy_type'])

    # Separate features (X) and target variable (y)
    X = data.drop(columns=['target'])  # Drop the target column from features
    y = data['target']  # Target is the 'target' column
    
    # Feature scaling (if necessary)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

# Step 3: Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Visualize the distribution of the target variable
    plt.figure(figsize=(6, 4))
    sns.countplot(x='target', data=data)
    plt.title("Claim Distribution")
    plt.xlabel("Target (Claim)")
    plt.ylabel("Count")
    plt.show()

    # Visualize correlations
    correlation_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

# Step 4: Model Building
def build_model(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)

    return model, X_test, y_test, y_pred

# Step 5: Model Evaluation
def evaluate_model(y_test, y_pred):
    # Print accuracy score
    print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.4f}")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=['No Claim', 'Claim'], yticklabels=['No Claim', 'Claim'])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

# Step 6: Main Function to Run Analysis
def main():
    # Load and preprocess the data
    data = load_data()
    X, y = preprocess_data(data)
    
    # Perform EDA
    perform_eda(data)
    
    # Build and evaluate the model
    model, X_test, y_test, y_pred = build_model(X, y)
    
    # Evaluate the model's performance
    evaluate_model(y_test, y_pred)

if __name__ == '__main__':
    main()
""",

    "product_recommendation": """def product_recommendation():
    print("Executing: Product Recommendation")
   # e_commerce_recommendation.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import seaborn as sns

# Step 1: Load the Dataset
def load_data():
    # Load the dataset (replace 'ecommerce_data.csv' with your actual dataset)
    data = pd.read_csv('ecommerce_data.csv')
    print("First 5 rows of the dataset:")
    print(data.head())
    return data

# Step 2: Data Preprocessing
def preprocess_data(data):
    # Handle missing values
    data.dropna(subset=['product_id', 'user_id', 'category'], inplace=True)

    # Create a user-product matrix
    user_product_matrix = data.pivot_table(index='user_id', columns='product_id', values='purchase_amount', fill_value=0)

    # Normalize the matrix
    return user_product_matrix

# Step 3: Collaborative Filtering using SVD (Singular Value Decomposition)
def collaborative_filtering(user_product_matrix):
    # Apply Singular Value Decomposition (SVD)
    svd = TruncatedSVD(n_components=50, random_state=42)
    svd_matrix = svd.fit_transform(user_product_matrix)

    # Calculate the predicted ratings for each user-product pair
    predicted_ratings = np.dot(svd_matrix, svd.components_)

    # Convert predicted ratings into a DataFrame
    predicted_ratings_df = pd.DataFrame(predicted_ratings, columns=user_product_matrix.columns)

    return predicted_ratings_df

# Step 4: Content-Based Filtering using Product Categories and TF-IDF
def content_based_filtering(data):
    # Vectorize product descriptions using TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['product_description'])

    # Compute cosine similarity between products based on descriptions
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim, data

# Step 5: Recommend Products (Collaborative Filtering)
def recommend_products_collaborative(predicted_ratings_df, user_id, num_recommendations=5):
    # Get the predicted ratings for the given user
    user_ratings = predicted_ratings_df.loc[user_id]

    # Sort the products by predicted rating in descending order
    recommended_products = user_ratings.sort_values(ascending=False).head(num_recommendations)

    return recommended_products

# Step 6: Recommend Products (Content-Based Filtering)
def recommend_products_content_based(cosine_sim, data, product_id, num_recommendations=5):
    # Get the index of the product
    product_index = data[data['product_id'] == product_id].index[0]

    # Get the pairwise similarity scores of all products with the given product
    sim_scores = list(enumerate(cosine_sim[product_index]))

    # Sort the products based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top N most similar products
    top_similar_products = sim_scores[1:num_recommendations+1]

    # Get the product IDs of the most similar products
    recommended_product_ids = [data['product_id'].iloc[i[0]] for i in top_similar_products]

    return recommended_product_ids

# Step 7: Main Function to Run the Recommendation System
def main():
    # Load and preprocess the data
    data = load_data()
    user_product_matrix = preprocess_data(data)

    # Collaborative Filtering: Predict ratings and recommend products for a user
    predicted_ratings_df = collaborative_filtering(user_product_matrix)
    user_id = 1  # Example user_id
    recommended_products_cf = recommend_products_collaborative(predicted_ratings_df, user_id)
    print(f"Recommended products for User {user_id} (Collaborative Filtering):")
    print(recommended_products_cf)

    # Content-Based Filtering: Recommend products based on similarity to a given product
    cosine_sim, data_with_descriptions = content_based_filtering(data)
    product_id = 101  # Example product_id
    recommended_products_cb = recommend_products_content_based(cosine_sim, data_with_descriptions, product_id)
    print(f"Recommended products for Product {product_id} (Content-Based Filtering):")
    print(recommended_products_cb)

if __name__ == '__main__':
    main()
""",

    "injury_prediction": """def injury_prediction():
    print("Executing: Injury Prediction")
    # sports_injury_prediction.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the dataset
def load_data():
    # Load the dataset (replace 'sports_injury_data.csv' with the actual dataset)
    data = pd.read_csv('sports_injury_data.csv')
    print("First 5 rows of the dataset:")
    print(data.head())
    return data

# Step 2: Data Preprocessing
def preprocess_data(data):
    # Handle missing values (fill with median or mean, drop if necessary)
    data.fillna(data.mean(), inplace=True)
    
    # Convert categorical columns to numerical using one-hot encoding (if any)
    data = pd.get_dummies(data, drop_first=True)

    # Normalize numerical features (scaling)
    scaler = StandardScaler()
    numerical_features = data.select_dtypes(include=['float64', 'int64']).columns
    data[numerical_features] = scaler.fit_transform(data[numerical_features])

    # Define target variable (binary classification: injury or not)
    X = data.drop('injury', axis=1)  # Features (exclude 'injury' column)
    y = data['injury']  # Target variable (1 if injury occurred, 0 if not)

    return X, y

# Step 3: Train-Test Split
def train_test_split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Step 4: Train Model (Random Forest / Logistic Regression)
def train_model(X_train, y_train):
    # Model 1: Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Model 2: Logistic Regression (optional for comparison)
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train, y_train)

    return rf_model, lr_model

# Step 5: Evaluate the model
def evaluate_model(model, X_test, y_test):
    # Make predictions
    y_pred = model.predict(X_test)

    # Classification Report
    print(f"Classification Report for {model.__class__.__name__}:")
    print(classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Injury', 'Injury'], yticklabels=['No Injury', 'Injury'])
    plt.title(f'Confusion Matrix for {model.__class__.__name__}')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    # ROC-AUC Score
    y_pred_prob = model.predict_proba(X_test)[:, 1]  # Probability of class 1 (injury)
    auc_score = roc_auc_score(y_test, y_pred_prob)
    print(f"ROC-AUC Score for {model.__class__.__name__}: {auc_score:.4f}")

# Step 6: Main function to run the model
def main():
    # Load and preprocess data
    data = load_data()
    X, y = preprocess_data(data)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)

    # Train the models
    rf_model, lr_model = train_model(X_train, y_train)

    # Evaluate Random Forest model
    evaluate_model(rf_model, X_test, y_test)

    # Evaluate Logistic Regression model (optional)
    evaluate_model(lr_model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "stock_price_prediction": """def stock_price_prediction():
    print("Executing: Stock Price Prediction")
    # stock_price_prediction.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

# Step 1: Load and preprocess data
def load_data():
    # Load the dataset (replace 'stock_data.csv' with the actual dataset)
    data = pd.read_csv('stock_data.csv')
    print("First 5 rows of the dataset:")
    print(data.head())
    
    # Keep relevant features: Date, Open, Close, Volume, etc.
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Use 'Close' price for prediction
    data = data[['Close']]
    return data

# Step 2: Feature Engineering
def create_features(data, window_size=60):
    features = []
    labels = []
    for i in range(window_size, len(data)):
        features.append(data[i-window_size:i, 0])  # Create sequences of length `window_size`
        labels.append(data[i, 0])  # Predict the next day's closing price
    return np.array(features), np.array(labels)

# Step 3: Normalize data
def normalize_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)
    return data_scaled, scaler

# Step 4: Train-Test Split
def train_test_split_data(data_scaled, window_size=60):
    X, y = create_features(data_scaled, window_size)
    
    # Split data into training and testing (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Reshape for LSTM (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    
    return X_train, X_test, y_train, y_test

# Step 5: Build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=1))  # Output layer with 1 neuron (next day's price)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Step 6: Train and Evaluate the LSTM model
def train_lstm_model(model, X_train, y_train, X_test, y_test, epochs=10, batch_size=32):
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[early_stopping])
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model's performance
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'Mean Squared Error (MSE): {mse}')
    print(f'R-squared: {r2}')
    
    return y_pred

# Step 7: Visualize the results
def visualize_results(y_test, y_pred):
    plt.figure(figsize=(10,6))
    plt.plot(y_test, color='blue', label='Actual Stock Price')
    plt.plot(y_pred, color='red', label='Predicted Stock Price')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

# Main function to run the model
def main():
    # Load and preprocess the data
    data = load_data()
    
    # Normalize data
    data_scaled, scaler = normalize_data(data.values)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split_data(data_scaled)
    
    # Build LSTM model
    model = build_lstm_model((X_train.shape[1], 1))
    
    # Train the model and get predictions
    y_pred = train_lstm_model(model, X_train, y_train, X_test, y_test)
    
    # Inverse the scaling for predictions
    y_pred_rescaled = scaler.inverse_transform(y_pred)
    y_test_rescaled = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Visualize results
    visualize_results(y_test_rescaled, y_pred_rescaled)

if __name__ == '__main__':
    main()
""",

    "dropout_prediction": """def dropout_prediction():
    print("Executing: Dropout Prediction")
    # student_dropout_prediction.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load and Preprocess the Data
def load_data():
    # Load the dataset (replace 'student_dropout.csv' with the actual dataset)
    data = pd.read_csv('student_dropout.csv')
    
    print("First 5 rows of the dataset:")
    print(data.head())
    
    # Handle missing values (fill with median or mode based on column type)
    data = data.fillna(data.median())  # For numerical columns
    data = data.apply(lambda x: x.fillna(x.mode()[0]), axis=0)  # For categorical columns

    # Convert categorical columns to numeric using LabelEncoder
    le = LabelEncoder()
    data['gender'] = le.fit_transform(data['gender'])  # Example: if gender is categorical
    # Add other categorical columns here if needed
    
    return data

# Step 2: Feature Engineering
def feature_engineering(data):
    # For this example, assume 'dropout' is the target column and the rest are features
    X = data.drop('dropout', axis=1)  # Drop 'dropout' column as it's the target
    y = data['dropout']  # Target column: dropout (binary classification)
    
    # Scale features if needed (e.g., grades or attendance might need scaling)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# Step 3: Train-Test Split
def train_test_split_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

# Step 4: Build and Train the Models
def train_models(X_train, y_train):
    # Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Logistic Regression
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train, y_train)
    
    return rf_model, lr_model

# Step 5: Evaluate the Models
def evaluate_models(models, X_test, y_test):
    rf_model, lr_model = models
    
    # Predictions
    rf_pred = rf_model.predict(X_test)
    lr_pred = lr_model.predict(X_test)
    
    # Evaluate Random Forest
    print("Random Forest Classification Report:")
    print(classification_report(y_test, rf_pred))
    print("Random Forest Confusion Matrix:")
    sns.heatmap(confusion_matrix(y_test, rf_pred), annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title("Random Forest Confusion Matrix")
    plt.show()

    # Evaluate Logistic Regression
    print("Logistic Regression Classification Report:")
    print(classification_report(y_test, lr_pred))
    print("Logistic Regression Confusion Matrix:")
    sns.heatmap(confusion_matrix(y_test, lr_pred), annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title("Logistic Regression Confusion Matrix")
    plt.show()

# Main function to run the workflow
def main():
    # Load and preprocess the data
    data = load_data()
    
    # Feature engineering
    X, y = feature_engineering(data)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    
    # Train models
    models = train_models(X_train, y_train)
    
    # Evaluate models
    evaluate_models(models, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "user_engagement_analysis": """def user_engagement_analysis():
    print("Executing: User Engagement Analysis")
    # social_media_engagement_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Step 1: Load and Preprocess the Data
def load_data():
    # Load the dataset (replace 'social_media_data.csv' with the actual dataset file)
    data = pd.read_csv('social_media_data.csv')
    
    print("First 5 rows of the dataset:")
    print(data.head())
    
    # Handle missing values
    data = data.fillna(data.median())  # Fill numerical columns with median
    data = data.apply(lambda x: x.fillna(x.mode()[0]), axis=0)  # Fill categorical columns with mode
    
    # Encode categorical columns (e.g., 'post_content_type', 'time_of_post')
    le = LabelEncoder()
    data['post_content_type'] = le.fit_transform(data['post_content_type'])  # Example encoding
    
    # Feature engineering: Extract time-based features if 'time_of_post' is in datetime format
    data['time_of_post'] = pd.to_datetime(data['time_of_post'])
    data['hour_of_day'] = data['time_of_post'].dt.hour
    data['day_of_week'] = data['time_of_post'].dt.dayofweek
    
    # Drop 'time_of_post' as it's now split into 'hour_of_day' and 'day_of_week'
    data = data.drop(['time_of_post'], axis=1)
    
    return data

# Step 2: Feature Engineering
def feature_engineering(data):
    # Separate features and target variable (engagement metrics: likes, comments, shares)
    X = data.drop(['likes', 'comments', 'shares'], axis=1)  # Drop engagement metrics from features
    y = data[['likes', 'comments', 'shares']]  # Target engagement columns
    
    # Normalize numerical features (e.g., likes, comments, shares)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# Step 3: Train-Test Split
def train_test_split_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

# Step 4: Build and Train the Model
def train_model(X_train, y_train):
    # Use Random Forest Regression to predict engagement metrics
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    return rf_model

# Step 5: Evaluate the Model
def evaluate_model(model, X_test, y_test):
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print("Evaluation Metrics:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-squared (R2): {r2}")
    
    # Visualize Actual vs Predicted values for each metric
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.scatter(y_test['likes'], y_pred[:, 0], color='blue', alpha=0.6)
    plt.title("Actual vs Predicted - Likes")
    plt.xlabel("Actual Likes")
    plt.ylabel("Predicted Likes")
    
    plt.subplot(1, 3, 2)
    plt.scatter(y_test['comments'], y_pred[:, 1], color='red', alpha=0.6)
    plt.title("Actual vs Predicted - Comments")
    plt.xlabel("Actual Comments")
    plt.ylabel("Predicted Comments")
    
    plt.subplot(1, 3, 3)
    plt.scatter(y_test['shares'], y_pred[:, 2], color='green', alpha=0.6)
    plt.title("Actual vs Predicted - Shares")
    plt.xlabel("Actual Shares")
    plt.ylabel("Predicted Shares")
    
    plt.tight_layout()
    plt.show()

# Step 6: Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Visualizing distribution of engagement metrics (likes, comments, shares)
    sns.histplot(data['likes'], kde=True, color='blue')
    plt.title('Distribution of Likes')
    plt.show()
    
    sns.histplot(data['comments'], kde=True, color='green')
    plt.title('Distribution of Comments')
    plt.show()
    
    sns.histplot(data['shares'], kde=True, color='red')
    plt.title('Distribution of Shares')
    plt.show()
    
    # Correlation heatmap to understand relationships between features and engagement metrics
    correlation_matrix = data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()

# Main function to run the workflow
def main():
    # Load and preprocess the data
    data = load_data()
    
    # Perform Exploratory Data Analysis (EDA)
    perform_eda(data)
    
    # Feature engineering
    X, y = feature_engineering(data)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    
    # Train the model
    rf_model = train_model(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(rf_model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "disease_outbreak_prediction": """def disease_outbreak_prediction():
    print("Executing: Disease Outbreak Prediction")
    # disease_outbreak_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Load and Preprocess the Data
def load_data():
    # Load the dataset (replace 'disease_outbreak_data.csv' with the actual dataset file)
    data = pd.read_csv('disease_outbreak_data.csv')
    
    print("First 5 rows of the dataset:")
    print(data.head())
    
    # Handle missing values (fill missing numerical values with median and categorical with mode)
    data = data.fillna(data.median())  # Fill numerical columns with median
    data = data.apply(lambda x: x.fillna(x.mode()[0]), axis=0)  # Fill categorical columns with mode
    
    # Encode categorical variables (if necessary)
    le = LabelEncoder()
    if 'location' in data.columns:
        data['location'] = le.fit_transform(data['location'])
    
    return data

# Step 2: Feature Engineering
def feature_engineering(data):
    # Features: weather conditions, location, and any relevant time-based data
    # Assuming the dataset includes 'temperature', 'humidity', 'precipitation', and 'outbreak'
    
    X = data.drop('outbreak', axis=1)  # Drop target variable 'outbreak'
    y = data['outbreak']  # Target variable: Outbreak (binary: 1 for outbreak, 0 for no outbreak)
    
    # Normalize numerical features (e.g., temperature, humidity, precipitation)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# Step 3: Train-Test Split
def train_test_split_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

# Step 4: Build and Train the Model
def train_model(X_train, y_train):
    # Use Random Forest Classifier to predict the outbreak likelihood
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    return rf_model

# Step 5: Evaluate the Model
def evaluate_model(model, X_test, y_test):
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion Matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['No Outbreak', 'Outbreak'], yticklabels=['No Outbreak', 'Outbreak'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# Step 6: Exploratory Data Analysis (EDA)
def perform_eda(data):
    # Visualizing the distribution of outbreaks
    sns.countplot(data['outbreak'], palette='Set2')
    plt.title('Distribution of Disease Outbreaks (0: No Outbreak, 1: Outbreak)')
    plt.show()
    
    # Visualize the relationship between weather and outbreaks (e.g., temperature vs outbreaks)
    sns.boxplot(x='outbreak', y='temperature', data=data)
    plt.title('Temperature vs Disease Outbreak')
    plt.show()
    
    sns.boxplot(x='outbreak', y='humidity', data=data)
    plt.title('Humidity vs Disease Outbreak')
    plt.show()
    
    sns.boxplot(x='outbreak', y='precipitation', data=data)
    plt.title('Precipitation vs Disease Outbreak')
    plt.show()

# Main function to run the workflow
def main():
    # Load and preprocess the data
    data = load_data()
    
    # Perform Exploratory Data Analysis (EDA)
    perform_eda(data)
    
    # Feature engineering
    X, y = feature_engineering(data)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    
    # Train the model
    rf_model = train_model(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(rf_model, X_test, y_test)

if __name__ == '__main__':
    main()
""",

    "tourist_behavior_analysis": """def tourist_behavior_analysis():
    print("Executing: Tourist Behavior Analysis")
    # tourist_behavior_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Step 1: Load and Preprocess Data
def load_data():
    # Load the dataset
    data = pd.read_csv('tourist_spending_data.csv')  # Replace with actual dataset file
    print("Dataset Preview:")
    print(data.head())

    # Handle missing values
    data = data.fillna(data.median())  # Replace missing numerical values with median

    # Select relevant features for clustering
    features = ['destination', 'duration_of_stay', 'spending']  # Adjust based on dataset
    if 'destination' in data.columns:
        data = pd.get_dummies(data, columns=['destination'], drop_first=True)

    return data, features

# Step 2: Normalize Data
def normalize_data(data, features):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[features])
    return scaled_data

# Step 3: Determine Optimal Number of Clusters
def find_optimal_clusters(data):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)

    # Elbow Method
    plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
    plt.title('Elbow Method')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.show()

    # Silhouette Score
    for n in range(2, 11):
        kmeans = KMeans(n_clusters=n, random_state=42)
        labels = kmeans.fit_predict(data)
        silhouette_avg = silhouette_score(data, labels)
        print(f"Silhouette Score for {n} clusters: {silhouette_avg:.2f}")

# Step 4: Perform Clustering
def perform_clustering(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data)
    return labels

# Step 5: Analyze Clusters
def analyze_clusters(data, labels):
    data['Cluster'] = labels
    print("Cluster Summary:")
    print(data.groupby('Cluster').mean())
    
    # Visualize Spending by Cluster
    sns.boxplot(x='Cluster', y='spending', data=data, palette='Set2')
    plt.title('Spending Distribution by Cluster')
    plt.show()

# Main Function
def main():
    # Load and preprocess data
    data, features = load_data()
    
    # Normalize data
    scaled_data = normalize_data(data, features)
    
    # Find the optimal number of clusters
    find_optimal_clusters(scaled_data)
    
    # Choose number of clusters (e.g., 3 based on elbow method or silhouette analysis)
    n_clusters = 3
    labels = perform_clustering(scaled_data, n_clusters)
    
    # Analyze clusters
    analyze_clusters(data, labels)

if __name__ == "__main__":
    main()
""",

    "ad_spend_optimization": """def ad_spend_optimization():
    print("Executing: Ad Spend Optimization")
   # Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
data = pd.read_csv("marketing_campaign_data.csv")  # Replace with actual file name

# Data Overview
print("Dataset Overview:")
print(data.info())
print(data.describe())

# Checking Missing Values
missing_values = data.isnull().sum()
print("\nMissing Values:\n", missing_values)

# Handle Missing Values (if any)
data.fillna(0, inplace=True)  # Replace with specific strategy as needed

# Calculate ROI for Each Channel
data['ROI'] = data['Conversions'] / data['Ad Spend']
print("\nData with ROI:\n", data[['Channel', 'Ad Spend', 'Impressions', 'Conversions', 'ROI']])

# Exploratory Data Analysis (EDA)
print("\nAd Spend Distribution:")
plt.figure(figsize=(10, 6))
sns.barplot(data=data, x='Channel', y='Ad Spend')
plt.title("Ad Spend by Channel")
plt.show()

print("\nROI Distribution:")
plt.figure(figsize=(10, 6))
sns.barplot(data=data, x='Channel', y='ROI')
plt.title("ROI by Channel")
plt.show()

# Identify High and Low-Performing Channels
high_roi_channels = data[data['ROI'] > data['ROI'].mean()]
low_roi_channels = data[data['ROI'] <= data['ROI'].mean()]

print("\nHigh ROI Channels:\n", high_roi_channels[['Channel', 'ROI']])
print("\nLow ROI Channels:\n", low_roi_channels[['Channel', 'ROI']])

# Optimization Recommendation: Allocate more budget to high ROI channels
recommended_budget_allocation = high_roi_channels[['Channel', 'Ad Spend', 'ROI']]
recommended_budget_allocation['Recommended Spend'] = recommended_budget_allocation['Ad Spend'] * 1.5  # Increase by 50%
print("\nRecommended Budget Allocation:\n", recommended_budget_allocation)

# Visualize Recommendation
plt.figure(figsize=(12, 6))
sns.barplot(data=recommended_budget_allocation, x='Channel', y='Recommended Spend')
plt.title("Recommended Budget Allocation")
plt.show()
""",

  "patient_outcome_prediction": """def patient_outcome_prediction():
    print("Executing: Patient Outcome Prediction")
    2.	Healthcare (Patient Outcome Prediction)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load Dataset
data_path = "hospital_readmissions.csv"  # Replace with your dataset path
data = pd.read_csv(data_path)

# Basic Data Exploration
print("Dataset Head:")
print(data.head())
print("\nDataset Info:")
data.info()
print("\nMissing Values:")
print(data.isnull().sum())

# Handle Missing Values (if any)
data = data.dropna()  # Simple approach: Drop rows with missing values

# Exploratory Data Analysis (EDA)
print("\nSummary Statistics:")
print(data.describe())

# Correlation Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Feature Selection
# Assuming the dataset has columns 'outcome' as target and other columns as features
X = data.drop("outcome", axis=1)  # Replace 'outcome' with your target column name
y = data["outcome"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Data Preprocessing
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Model Evaluation
y_pred = model.predict(X_test)
print("\nAccuracy Score:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Feature Importance
feature_importances = pd.DataFrame(
    model.feature_importances_, index=X.columns, columns=["Importance"]
).sort_values(by="Importance", ascending=False)

print("\nFeature Importances:")
print(feature_importances)

# Save Model (optional)
import joblib
joblib.dump(model, "patient_outcome_predictor.pkl")

# How to Use the Model
# Load the model and make predictions
# loaded_model = joblib.load("patient_outcome_predictor.pkl")
# predictions = loaded_model.predict(new_data)
""",

"data_load": """def dataload():
    print("Executing: Types of Load")
    # You can load data from different types of files
    # Example for loading from CSV, Excel, JSON, SQL, etc.
    def load_input_data(file_path, file_type='csv'):
        print(f"Loading data from {file_path} ({file_type})")

        # Handle different file types
        if file_type == 'csv':
            import pandas as pd
            data = pd.read_csv(file_path)

        elif file_type == 'excel':
            import pandas as pd
            data = pd.read_excel(file_path)

        elif file_type == 'json':
            import pandas as pd
            data = pd.read_json(file_path)

        elif file_type == 'sql':
            import sqlite3
            conn = sqlite3.connect(file_path)
            query = "SELECT * FROM data"  # Adjust this query based on your table name
            data = pd.read_sql(query, conn)
            conn.close()

        else:
            raise ValueError("Unsupported file type")

        # Display the first few rows of the loaded data
        print("Loaded Data:")
        print(data.head())
        return data"""



}

def get_unique_code_snippet(function_name):
    snippet = unique_code_snippets.get(function_name)
    if snippet:
        return snippet
    else:
        return f"No unique code snippet found for {function_name}."
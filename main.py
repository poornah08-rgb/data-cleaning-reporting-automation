import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("output", exist_ok=True)

# Load dataset
input_file = "student_performance.csv"

print("DATA CLEANING AND REPORTING AUTOMATION")
print("=" * 45)

try:
    df = pd.read_csv(input_file)

    print("\nOriginal Dataset:")
    print(df.head())

    # Original dataset information
    original_rows = len(df)
    original_columns = len(df.columns)

    # Remove duplicate rows
    duplicates_removed = df.duplicated().sum()
    df = df.drop_duplicates()

    # Handle missing values
    missing_values_before = int(df.isnull().sum().sum())

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            median_value = df[column].median()

            if pd.notna(median_value):
                df[column] = df[column].fillna(median_value)
        else:
            mode_value = df[column].mode(dropna=True)

            if not mode_value.empty:
                df[column] = df[column].fillna(mode_value.iloc[0])
            else:
                df[column] = df[column].fillna("Unknown")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Standardize text values
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    # Save cleaned dataset
    cleaned_file = "output/cleaned_student_performance.csv"
    df.to_csv(cleaned_file, index=False)

    # Generate descriptive statistics
    numeric_data = df.select_dtypes(include=["number"])
    statistics = numeric_data.describe()

    statistics.to_csv("output/descriptive_statistics.csv")

    # Generate automated text report
    report_file = "output/cleaning_report.txt"

    with open(report_file, "w", encoding="utf-8") as report:
        report.write("DATA CLEANING AND REPORTING AUTOMATION\n")
        report.write("=" * 45 + "\n\n")

        report.write(f"Original number of rows: {original_rows}\n")
        report.write(f"Number of columns: {original_columns}\n")
        report.write(f"Duplicate rows removed: {duplicates_removed}\n")
        report.write(
            f"Missing values before cleaning: {missing_values_before}\n"
        )
        report.write(f"Rows after cleaning: {len(df)}\n")
        report.write(f"Columns after cleaning: {len(df.columns)}\n")
        report.write(
            f"Missing values after cleaning: {int(df.isnull().sum().sum())}\n"
        )

        report.write("\nCLEANED DATA PREVIEW\n")
        report.write("-" * 30 + "\n")
        report.write(df.head().to_string(index=False))

        report.write("\n\nDESCRIPTIVE STATISTICS\n")
        report.write("-" * 30 + "\n")
        report.write(statistics.to_string())

        report.write("\n\nCONCLUSION\n")
        report.write(
            "The dataset was processed using Python and Pandas. "
            "Duplicate rows were removed, missing values were handled, "
            "text fields were standardized, and reports were generated."
        )

    # Create visual summaries for numeric columns
    if not numeric_data.empty:
        numeric_data.hist(figsize=(12, 8), bins=10)
        plt.suptitle("Student Performance - Data Distribution")
        plt.tight_layout()

        chart_file = "output/data_distribution.png"
        plt.savefig(chart_file, dpi=150, bbox_inches="tight")
        plt.close()

        # Correlation heatmap without requiring Seaborn
        correlation = numeric_data.corr()

        if not correlation.empty:
            plt.figure(figsize=(8, 6))

            image = plt.imshow(
                correlation,
                cmap="coolwarm",
                vmin=-1,
                vmax=1
            )

            plt.colorbar(image)
            plt.xticks(
                range(len(correlation.columns)),
                correlation.columns,
                rotation=45,
                ha="right"
            )
            plt.yticks(
                range(len(correlation.columns)),
                correlation.columns
            )

            plt.title("Correlation Between Numeric Features")
            plt.tight_layout()

            plt.savefig(
                "output/correlation_heatmap.png",
                dpi=150,
                bbox_inches="tight"
            )

            plt.close()

    print("\nData cleaning completed successfully!")
    print("\nReport Summary")
    print("-" * 30)
    print("Original rows:", original_rows)
    print("Duplicate rows removed:", duplicates_removed)
    print("Missing values before cleaning:", missing_values_before)
    print("Rows after cleaning:", len(df))
    print("Missing values after cleaning:", int(df.isnull().sum().sum()))

    print("\nGenerated files:")
    print("- output/cleaned_student_performance.csv")
    print("- output/descriptive_statistics.csv")
    print("- output/cleaning_report.txt")

    if not numeric_data.empty:
        print("- output/data_distribution.png")
        print("- output/correlation_heatmap.png")

except FileNotFoundError:
    print("Error: student_performance.csv was not found.")
    print("Please upload the CSV file into the repository.")

except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")

except pd.errors.ParserError:
    print("Error: The CSV file format is invalid.")

except Exception as error:
    print("An unexpected error occurred:", error)

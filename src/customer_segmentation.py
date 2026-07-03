from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def customer_segmentation(df):

    customer_data = df.groupby("Customer Name").agg({
        "Sales":    "sum",
        "Profit":   "sum",
        "Quantity": "sum",
    }).reset_index()

    n_customers = len(customer_data)

    # ── Guard: need at least 2 customers to cluster ────────────
    # KMeans crashes if n_samples < n_clusters.
    # Dynamically reduce clusters to fit however many rows we have.
    # Min 2 so scatter still shows distinct groups.
    if n_customers < 2:
        customer_data["Cluster"] = "Segment 1"
        return customer_data

    n_clusters = min(4, n_customers)

    X = customer_data[["Sales", "Profit", "Quantity"]]

    # ── Scale features so large Sales values don't dominate ────
    # Without scaling, KMeans groups by Sales magnitude only
    # because Sales (~$10k) dwarfs Quantity (~5 units).
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    customer_data["Cluster"] = model.fit_predict(X_scaled).astype(str)

    # Rename clusters to human-readable labels
    label_map = {"0": "Segment A", "1": "Segment B",
                 "2": "Segment C", "3": "Segment D"}
    customer_data["Cluster"] = customer_data["Cluster"].map(
        lambda c: label_map.get(c, f"Segment {c}")
    )

    return customer_data
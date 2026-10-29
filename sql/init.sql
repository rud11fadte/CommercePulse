CREATE TABLE IF NOT EXISTS monthly_order_analytics (
    purchase_month VARCHAR(7) NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    order_count INTEGER NOT NULL CHECK (order_count >= 0),
    PRIMARY KEY (purchase_month, order_status)
);

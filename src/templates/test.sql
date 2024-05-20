CREATE TABLE mainapp_paymentcard (
    card_id SERIAL PRIMARY KEY,
    name VARCHAR(255) DEFAULT '',
    card_holder_name VARCHAR(255) NOT NULL,
    card_type VARCHAR(100) NOT NULL,
    card_number VARCHAR(50) NOT NULL,
    card_no_last_four VARCHAR(50) DEFAULT NULL,
    cvv VARCHAR(10) NOT NULL,
    expiration_date DATE DEFAULT NULL,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    author VARCHAR(255),
    tags TEXT[],
    source_url TEXT,
    scraped_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (text, author)
);

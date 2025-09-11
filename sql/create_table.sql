-- create_tables.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS farmers (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name text,
  phone text UNIQUE,
  language text DEFAULT 'en',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS farms (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  farmer_id uuid REFERENCES farmers(id) ON DELETE CASCADE,
  name text,
  polygon_json jsonb DEFAULT '{}'::jsonb,
  area_ha numeric,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS images (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  farm_id uuid,
  farmer_id uuid,
  s3_path text,
  metadata jsonb,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS recommendations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  farm_id uuid,
  created_by uuid,
  request jsonb,
  response jsonb,
  model_version text,
  created_at timestamptz DEFAULT now()
);

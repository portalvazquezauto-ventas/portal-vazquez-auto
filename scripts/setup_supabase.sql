-- ============================================================
-- Portal Vázquez Auto — Setup SQL
-- Ejecutar en Supabase SQL Editor (en orden)
-- ============================================================

-- ── TABLAS ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('director', 'manager', 'seller')),
  email TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE,
  must_change_password BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS manual_sections (
  id SERIAL PRIMARY KEY,
  section_number TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  quiz_questions JSONB DEFAULT '[]',
  last_updated TIMESTAMPTZ DEFAULT NOW(),
  updated_by UUID REFERENCES profiles(id)
);

CREATE TABLE IF NOT EXISTS manual_reads (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  section_id INTEGER REFERENCES manual_sections(id) ON DELETE CASCADE,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  quiz_answers JSONB DEFAULT '{}',
  quiz_score INTEGER,
  is_completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS notifications (
  id SERIAL PRIMARY KEY,
  recipient_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  sender_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  body TEXT,
  payload JSONB DEFAULT '{}',
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS training_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  profile_type TEXT NOT NULL,
  mode TEXT NOT NULL CHECK (mode IN ('training', 'evaluation')),
  messages JSONB DEFAULT '[]',
  score_indagacion INTEGER,
  score_objeciones INTEGER,
  score_consultivo INTEGER,
  score_global INTEGER,
  feedback_final TEXT,
  used_hints BOOLEAN DEFAULT FALSE,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  is_completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS question_guide (
  id SERIAL PRIMARY KEY,
  profile_type TEXT NOT NULL,
  category TEXT NOT NULL,
  question TEXT NOT NULL,
  expected_answer TEXT NOT NULL,
  manual_reference TEXT,
  order_index INTEGER DEFAULT 0
);

-- ── ROW LEVEL SECURITY ──────────────────────────────────────

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE manual_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE manual_reads ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_guide ENABLE ROW LEVEL SECURITY;

-- Helper: obtener el rol del usuario actual
CREATE OR REPLACE FUNCTION get_my_role()
RETURNS TEXT AS $$
  SELECT role FROM profiles WHERE id = auth.uid();
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- ── POLICIES: profiles ───────────────────────────────────────

DROP POLICY IF EXISTS "profiles_select" ON profiles;
CREATE POLICY "profiles_select" ON profiles FOR SELECT
  USING (
    auth.uid() = id
    OR get_my_role() IN ('director', 'manager')
  );

DROP POLICY IF EXISTS "profiles_insert" ON profiles;
CREATE POLICY "profiles_insert" ON profiles FOR INSERT
  WITH CHECK (get_my_role() IN ('director', 'manager'));

DROP POLICY IF EXISTS "profiles_update" ON profiles;
CREATE POLICY "profiles_update" ON profiles FOR UPDATE
  USING (
    auth.uid() = id
    OR get_my_role() IN ('director', 'manager')
  );

-- ── POLICIES: manual_sections ────────────────────────────────

DROP POLICY IF EXISTS "manual_sections_select" ON manual_sections;
CREATE POLICY "manual_sections_select" ON manual_sections FOR SELECT
  USING (true);

DROP POLICY IF EXISTS "manual_sections_insert" ON manual_sections;
CREATE POLICY "manual_sections_insert" ON manual_sections FOR INSERT
  WITH CHECK (get_my_role() IN ('director', 'manager'));

DROP POLICY IF EXISTS "manual_sections_update" ON manual_sections;
CREATE POLICY "manual_sections_update" ON manual_sections FOR UPDATE
  USING (get_my_role() IN ('director', 'manager'));

-- ── POLICIES: manual_reads ────────────────────────────────────

DROP POLICY IF EXISTS "manual_reads_select" ON manual_reads;
CREATE POLICY "manual_reads_select" ON manual_reads FOR SELECT
  USING (
    auth.uid() = user_id
    OR get_my_role() IN ('director', 'manager')
  );

DROP POLICY IF EXISTS "manual_reads_insert" ON manual_reads;
CREATE POLICY "manual_reads_insert" ON manual_reads FOR INSERT
  WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "manual_reads_update" ON manual_reads;
CREATE POLICY "manual_reads_update" ON manual_reads FOR UPDATE
  USING (auth.uid() = user_id);

-- ── POLICIES: notifications ───────────────────────────────────

DROP POLICY IF EXISTS "notifications_select" ON notifications;
CREATE POLICY "notifications_select" ON notifications FOR SELECT
  USING (
    auth.uid() = recipient_id
    OR get_my_role() = 'director'
  );

DROP POLICY IF EXISTS "notifications_insert" ON notifications;
CREATE POLICY "notifications_insert" ON notifications FOR INSERT
  WITH CHECK (true);

DROP POLICY IF EXISTS "notifications_update" ON notifications;
CREATE POLICY "notifications_update" ON notifications FOR UPDATE
  USING (
    auth.uid() = recipient_id
    OR get_my_role() = 'director'
  );

-- ── POLICIES: training_sessions ───────────────────────────────

DROP POLICY IF EXISTS "training_sessions_select" ON training_sessions;
CREATE POLICY "training_sessions_select" ON training_sessions FOR SELECT
  USING (
    auth.uid() = user_id
    OR get_my_role() IN ('director', 'manager')
  );

DROP POLICY IF EXISTS "training_sessions_insert" ON training_sessions;
CREATE POLICY "training_sessions_insert" ON training_sessions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "training_sessions_update" ON training_sessions;
CREATE POLICY "training_sessions_update" ON training_sessions FOR UPDATE
  USING (auth.uid() = user_id);

-- ── POLICIES: question_guide ──────────────────────────────────

DROP POLICY IF EXISTS "question_guide_select" ON question_guide;
CREATE POLICY "question_guide_select" ON question_guide FOR SELECT
  USING (true);

DROP POLICY IF EXISTS "question_guide_insert" ON question_guide;
CREATE POLICY "question_guide_insert" ON question_guide FOR INSERT
  WITH CHECK (get_my_role() IN ('director', 'manager'));

DROP POLICY IF EXISTS "question_guide_update" ON question_guide;
CREATE POLICY "question_guide_update" ON question_guide FOR UPDATE
  USING (get_my_role() IN ('director', 'manager'));

-- ── TRIGGER: crear profile al crear usuario auth ─────────────

CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, full_name, role, email)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
    COALESCE(NEW.raw_user_meta_data->>'role', 'seller'),
    NEW.email
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

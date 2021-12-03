--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activities (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.activities OWNER TO postgres;

--
-- Name: activities_activities_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activities_activities_connections (
    activity character varying(32),
    top_level_activity character varying(32)
);


ALTER TABLE public.activities_activities_connections OWNER TO postgres;

--
-- Name: activities_targets_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activities_targets_connections (
    activity character varying(32),
    target character varying(32)
);


ALTER TABLE public.activities_targets_connections OWNER TO postgres;

--
-- Name: competences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competences (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.competences OWNER TO postgres;

--
-- Name: competences_competences_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competences_competences_connections (
    competence character varying(32),
    top_level_competence character varying(32)
);


ALTER TABLE public.competences_competences_connections OWNER TO postgres;

--
-- Name: competences_knowledges_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competences_knowledges_connections (
    competence character varying(32),
    knowledge character varying(32)
);


ALTER TABLE public.competences_knowledges_connections OWNER TO postgres;

--
-- Name: competences_skills_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competences_skills_connections (
    competence character varying(32),
    skill character varying(32)
);


ALTER TABLE public.competences_skills_connections OWNER TO postgres;

--
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.courses OWNER TO postgres;

--
-- Name: knowledges; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knowledges (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.knowledges OWNER TO postgres;

--
-- Name: knowledges_quantums_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knowledges_quantums_connections (
    knowledge character varying(32),
    quantum character varying(32)
);


ALTER TABLE public.knowledges_quantums_connections OWNER TO postgres;

--
-- Name: knowledges_themes_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knowledges_themes_connections (
    knowledge character varying(32),
    theme character varying(32)
);


ALTER TABLE public.knowledges_themes_connections OWNER TO postgres;

--
-- Name: metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metrics (
    id character varying(32) NOT NULL,
    name text,
    description text
);


ALTER TABLE public.metrics OWNER TO postgres;

--
-- Name: professions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.professions (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.professions OWNER TO postgres;

--
-- Name: professions_competences_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.professions_competences_connections (
    profession character varying(32),
    competence character varying(32)
);


ALTER TABLE public.professions_competences_connections OWNER TO postgres;

--
-- Name: quantums; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quantums (
    id character varying(32) NOT NULL,
    name text,
    description text
);


ALTER TABLE public.quantums OWNER TO postgres;

--
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.skills OWNER TO postgres;

--
-- Name: skills_activities_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills_activities_connections (
    skill character varying(32),
    activity character varying(32)
);


ALTER TABLE public.skills_activities_connections OWNER TO postgres;

--
-- Name: suos_competences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suos_competences (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.suos_competences OWNER TO postgres;

--
-- Name: suos_competences_competences_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suos_competences_competences_connections (
    suos_competence character varying(32),
    competence character varying(32)
);


ALTER TABLE public.suos_competences_competences_connections OWNER TO postgres;

--
-- Name: targets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.targets (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.targets OWNER TO postgres;

--
-- Name: targets_knowledges_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.targets_knowledges_connections (
    target character varying(32),
    knowledge character varying(32)
);


ALTER TABLE public.targets_knowledges_connections OWNER TO postgres;

--
-- Name: targets_metrics_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.targets_metrics_connections (
    target character varying(32),
    metric character varying(32)
);


ALTER TABLE public.targets_metrics_connections OWNER TO postgres;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id character varying(32) NOT NULL,
    name text,
    description text
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_targets_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks_targets_connections (
    task character varying(32),
    target character varying(32)
);


ALTER TABLE public.tasks_targets_connections OWNER TO postgres;

--
-- Name: themes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.themes (
    id character varying(32) NOT NULL,
    name text
);


ALTER TABLE public.themes OWNER TO postgres;

--
-- Name: themes_courses_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.themes_courses_connections (
    theme character varying(32),
    course character varying(32)
);


ALTER TABLE public.themes_courses_connections OWNER TO postgres;

--
-- Name: themes_themes_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.themes_themes_connections (
    theme character varying(32),
    top_level_theme character varying(32)
);


ALTER TABLE public.themes_themes_connections OWNER TO postgres;

--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: competences competences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competences
    ADD CONSTRAINT competences_pkey PRIMARY KEY (id);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: knowledges knowledges_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knowledges
    ADD CONSTRAINT knowledges_pkey PRIMARY KEY (id);


--
-- Name: metrics metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_pkey PRIMARY KEY (id);


--
-- Name: professions professions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.professions
    ADD CONSTRAINT professions_pkey PRIMARY KEY (id);


--
-- Name: quantums quantums_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quantums
    ADD CONSTRAINT quantums_pkey PRIMARY KEY (id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: suos_competences suos_competences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suos_competences
    ADD CONSTRAINT suos_competences_pkey PRIMARY KEY (id);


--
-- Name: targets targets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: themes themes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.themes
    ADD CONSTRAINT themes_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--


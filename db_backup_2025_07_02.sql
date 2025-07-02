--
-- PostgreSQL database dump
--

-- Dumped from database version 14.12 (Debian 14.12-1.pgdg120+1)
-- Dumped by pg_dump version 14.12 (Debian 14.12-1.pgdg120+1)

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
-- Name: auth_group; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO dspop_user;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO dspop_user;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO dspop_user;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO dspop_user;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO dspop_user;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO dspop_user;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authentication_customuser; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.authentication_customuser (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    pj_number character varying(150) NOT NULL,
    phone character varying(150) NOT NULL,
    mobile character varying(150) NOT NULL
);


ALTER TABLE public.authentication_customuser OWNER TO dspop_user;

--
-- Name: authentication_customuser_departments; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.authentication_customuser_departments (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    department_id bigint NOT NULL
);


ALTER TABLE public.authentication_customuser_departments OWNER TO dspop_user;

--
-- Name: authentication_customuser_departments_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.authentication_customuser_departments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authentication_customuser_departments_id_seq OWNER TO dspop_user;

--
-- Name: authentication_customuser_departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.authentication_customuser_departments_id_seq OWNED BY public.authentication_customuser_departments.id;


--
-- Name: authentication_customuser_groups; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.authentication_customuser_groups (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.authentication_customuser_groups OWNER TO dspop_user;

--
-- Name: authentication_customuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.authentication_customuser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authentication_customuser_groups_id_seq OWNER TO dspop_user;

--
-- Name: authentication_customuser_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.authentication_customuser_groups_id_seq OWNED BY public.authentication_customuser_groups.id;


--
-- Name: authentication_customuser_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.authentication_customuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authentication_customuser_id_seq OWNER TO dspop_user;

--
-- Name: authentication_customuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.authentication_customuser_id_seq OWNED BY public.authentication_customuser.id;


--
-- Name: authentication_customuser_user_permissions; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.authentication_customuser_user_permissions (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.authentication_customuser_user_permissions OWNER TO dspop_user;

--
-- Name: authentication_customuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.authentication_customuser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authentication_customuser_user_permissions_id_seq OWNER TO dspop_user;

--
-- Name: authentication_customuser_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.authentication_customuser_user_permissions_id_seq OWNED BY public.authentication_customuser_user_permissions.id;


--
-- Name: budget_budgetcategory; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.budget_budgetcategory (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(20) NOT NULL
);


ALTER TABLE public.budget_budgetcategory OWNER TO dspop_user;

--
-- Name: budget_budgetcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.budget_budgetcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_budgetcategory_id_seq OWNER TO dspop_user;

--
-- Name: budget_budgetcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.budget_budgetcategory_id_seq OWNED BY public.budget_budgetcategory.id;


--
-- Name: budget_financialyear; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.budget_financialyear (
    id bigint NOT NULL,
    name character varying(20) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
);


ALTER TABLE public.budget_financialyear OWNER TO dspop_user;

--
-- Name: budget_financialyear_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.budget_financialyear_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_financialyear_id_seq OWNER TO dspop_user;

--
-- Name: budget_financialyear_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.budget_financialyear_id_seq OWNED BY public.budget_financialyear.id;


--
-- Name: budget_performanceindicator; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.budget_performanceindicator (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    baseline character varying(100) NOT NULL,
    target character varying(100) NOT NULL,
    measurement_frequency character varying(50) NOT NULL,
    workplan_item_id bigint NOT NULL
);


ALTER TABLE public.budget_performanceindicator OWNER TO dspop_user;

--
-- Name: budget_performanceindicator_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.budget_performanceindicator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_performanceindicator_id_seq OWNER TO dspop_user;

--
-- Name: budget_performanceindicator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.budget_performanceindicator_id_seq OWNED BY public.budget_performanceindicator.id;


--
-- Name: budget_quarterlyallocation; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.budget_quarterlyallocation (
    id bigint NOT NULL,
    quarter integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    workplan_item_id bigint NOT NULL
);


ALTER TABLE public.budget_quarterlyallocation OWNER TO dspop_user;

--
-- Name: budget_quarterlyallocation_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.budget_quarterlyallocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_quarterlyallocation_id_seq OWNER TO dspop_user;

--
-- Name: budget_quarterlyallocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.budget_quarterlyallocation_id_seq OWNED BY public.budget_quarterlyallocation.id;


--
-- Name: budget_transformativeinitiative; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.budget_transformativeinitiative (
    id bigint NOT NULL,
    implementation_status character varying(100) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    progress integer NOT NULL,
    workplan_item_id bigint NOT NULL
);


ALTER TABLE public.budget_transformativeinitiative OWNER TO dspop_user;

--
-- Name: budget_transformativeinitiative_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.budget_transformativeinitiative_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_transformativeinitiative_id_seq OWNER TO dspop_user;

--
-- Name: budget_transformativeinitiative_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.budget_transformativeinitiative_id_seq OWNED BY public.budget_transformativeinitiative.id;


--
-- Name: budget_workplanitem; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.budget_workplanitem (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    budget_code character varying(20) NOT NULL,
    description text NOT NULL,
    item_type character varying(20) NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    category_id bigint NOT NULL,
    financial_year_id bigint NOT NULL
);


ALTER TABLE public.budget_workplanitem OWNER TO dspop_user;

--
-- Name: budget_workplanitem_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.budget_workplanitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_workplanitem_id_seq OWNER TO dspop_user;

--
-- Name: budget_workplanitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.budget_workplanitem_id_seq OWNED BY public.budget_workplanitem.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO dspop_user;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO dspop_user;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO dspop_user;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO dspop_user;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO dspop_user;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO dspop_user;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO dspop_user;

--
-- Name: document_management_document; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.document_management_document (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    file character varying(100),
    file_type character varying(50) NOT NULL,
    file_size bigint NOT NULL,
    tags character varying(500) NOT NULL,
    storage_type character varying(20) NOT NULL,
    drive_file_id character varying(100),
    drive_view_link character varying(200),
    is_confidential boolean NOT NULL,
    status character varying(20) NOT NULL,
    password_protected boolean NOT NULL,
    access_code character varying(100),
    object_id integer,
    source_module character varying(50) NOT NULL,
    version character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    last_accessed timestamp with time zone,
    expiry_date timestamp with time zone,
    category_id bigint,
    content_type_id integer,
    parent_document_id bigint,
    uploaded_by_id bigint NOT NULL,
    CONSTRAINT document_management_document_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.document_management_document OWNER TO dspop_user;

--
-- Name: document_management_document_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.document_management_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_management_document_id_seq OWNER TO dspop_user;

--
-- Name: document_management_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.document_management_document_id_seq OWNED BY public.document_management_document.id;


--
-- Name: document_management_documentaccess; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.document_management_documentaccess (
    id bigint NOT NULL,
    permission_type character varying(20) NOT NULL,
    granted_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone,
    is_active boolean NOT NULL,
    document_id bigint NOT NULL,
    granted_by_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.document_management_documentaccess OWNER TO dspop_user;

--
-- Name: document_management_documentaccess_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.document_management_documentaccess_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_management_documentaccess_id_seq OWNER TO dspop_user;

--
-- Name: document_management_documentaccess_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.document_management_documentaccess_id_seq OWNED BY public.document_management_documentaccess.id;


--
-- Name: document_management_documentactivity; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.document_management_documentactivity (
    id bigint NOT NULL,
    action character varying(20) NOT NULL,
    action_details text NOT NULL,
    ip_address inet,
    user_agent character varying(500) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    document_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.document_management_documentactivity OWNER TO dspop_user;

--
-- Name: document_management_documentactivity_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.document_management_documentactivity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_management_documentactivity_id_seq OWNER TO dspop_user;

--
-- Name: document_management_documentactivity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.document_management_documentactivity_id_seq OWNED BY public.document_management_documentactivity.id;


--
-- Name: document_management_documentcategory; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.document_management_documentcategory (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.document_management_documentcategory OWNER TO dspop_user;

--
-- Name: document_management_documentcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.document_management_documentcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_management_documentcategory_id_seq OWNER TO dspop_user;

--
-- Name: document_management_documentcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.document_management_documentcategory_id_seq OWNED BY public.document_management_documentcategory.id;


--
-- Name: document_management_documentcomment; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.document_management_documentcomment (
    id bigint NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    author_id bigint NOT NULL,
    document_id bigint NOT NULL,
    parent_comment_id bigint
);


ALTER TABLE public.document_management_documentcomment OWNER TO dspop_user;

--
-- Name: document_management_documentcomment_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.document_management_documentcomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_management_documentcomment_id_seq OWNER TO dspop_user;

--
-- Name: document_management_documentcomment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.document_management_documentcomment_id_seq OWNED BY public.document_management_documentcomment.id;


--
-- Name: home_module; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.home_module (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    icon_class character varying(100) NOT NULL,
    url_name character varying(200) NOT NULL,
    permission_codename character varying(150) NOT NULL
);


ALTER TABLE public.home_module OWNER TO dspop_user;

--
-- Name: home_module_departments; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.home_module_departments (
    id bigint NOT NULL,
    module_id bigint NOT NULL,
    department_id bigint NOT NULL
);


ALTER TABLE public.home_module_departments OWNER TO dspop_user;

--
-- Name: home_module_departments_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.home_module_departments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.home_module_departments_id_seq OWNER TO dspop_user;

--
-- Name: home_module_departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.home_module_departments_id_seq OWNED BY public.home_module_departments.id;


--
-- Name: home_module_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.home_module_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.home_module_id_seq OWNER TO dspop_user;

--
-- Name: home_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.home_module_id_seq OWNED BY public.home_module.id;


--
-- Name: innovations_innovation; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.innovations_innovation (
    id bigint NOT NULL,
    station character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    is_replication boolean NOT NULL,
    source_court character varying(255),
    category character varying(100) NOT NULL,
    situation_before text NOT NULL,
    description text NOT NULL,
    solution text NOT NULL,
    replication_potential text NOT NULL,
    individuals_involved text NOT NULL,
    stakeholders_affected text NOT NULL,
    status character varying(20) NOT NULL,
    submitted_at timestamp with time zone NOT NULL,
    approved_at timestamp with time zone,
    approved_by_id bigint,
    court_id bigint NOT NULL,
    financial_year_id bigint NOT NULL,
    submitted_by_id bigint
);


ALTER TABLE public.innovations_innovation OWNER TO dspop_user;

--
-- Name: innovations_innovation_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.innovations_innovation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.innovations_innovation_id_seq OWNER TO dspop_user;

--
-- Name: innovations_innovation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.innovations_innovation_id_seq OWNED BY public.innovations_innovation.id;


--
-- Name: innovations_innovationattachment; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.innovations_innovationattachment (
    id bigint NOT NULL,
    file character varying(100) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    innovation_id bigint NOT NULL,
    uploaded_by_id bigint
);


ALTER TABLE public.innovations_innovationattachment OWNER TO dspop_user;

--
-- Name: innovations_innovationattachment_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.innovations_innovationattachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.innovations_innovationattachment_id_seq OWNER TO dspop_user;

--
-- Name: innovations_innovationattachment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.innovations_innovationattachment_id_seq OWNED BY public.innovations_innovationattachment.id;


--
-- Name: mail_mailactivity; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.mail_mailactivity (
    id bigint NOT NULL,
    action character varying(20) NOT NULL,
    notes text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    location character varying(255) NOT NULL,
    mail_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.mail_mailactivity OWNER TO dspop_user;

--
-- Name: mail_mailactivity_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.mail_mailactivity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_mailactivity_id_seq OWNER TO dspop_user;

--
-- Name: mail_mailactivity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.mail_mailactivity_id_seq OWNED BY public.mail_mailactivity.id;


--
-- Name: mail_mailassignment; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.mail_mailassignment (
    id bigint NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    due_date date,
    completed boolean NOT NULL,
    completed_at timestamp with time zone,
    notes text NOT NULL,
    current_location character varying(255) NOT NULL,
    acknowledgment_required boolean NOT NULL,
    acknowledged boolean NOT NULL,
    acknowledged_at timestamp with time zone,
    acknowledged_by character varying(255) NOT NULL,
    assigned_by_id bigint NOT NULL,
    assigned_to_id bigint NOT NULL,
    mail_id bigint NOT NULL
);


ALTER TABLE public.mail_mailassignment OWNER TO dspop_user;

--
-- Name: mail_mailassignment_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.mail_mailassignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_mailassignment_id_seq OWNER TO dspop_user;

--
-- Name: mail_mailassignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.mail_mailassignment_id_seq OWNED BY public.mail_mailassignment.id;


--
-- Name: mail_mailattachment; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.mail_mailattachment (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    attachment_type character varying(100) NOT NULL,
    quantity integer NOT NULL,
    condition character varying(100) NOT NULL,
    digital_copy_id bigint,
    mail_id bigint NOT NULL,
    CONSTRAINT mail_mailattachment_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.mail_mailattachment OWNER TO dspop_user;

--
-- Name: mail_mailattachment_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.mail_mailattachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_mailattachment_id_seq OWNER TO dspop_user;

--
-- Name: mail_mailattachment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.mail_mailattachment_id_seq OWNED BY public.mail_mailattachment.id;


--
-- Name: mail_mailmovement; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.mail_mailmovement (
    id bigint NOT NULL,
    from_location character varying(255) NOT NULL,
    to_location character varying(255) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    notes text NOT NULL,
    received_by character varying(255) NOT NULL,
    received_at timestamp with time zone,
    handler_id bigint NOT NULL,
    mail_id bigint NOT NULL
);


ALTER TABLE public.mail_mailmovement OWNER TO dspop_user;

--
-- Name: mail_mailmovement_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.mail_mailmovement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_mailmovement_id_seq OWNER TO dspop_user;

--
-- Name: mail_mailmovement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.mail_mailmovement_id_seq OWNED BY public.mail_mailmovement.id;


--
-- Name: mail_physicalmail; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.mail_physicalmail (
    id bigint NOT NULL,
    tracking_number character varying(100) NOT NULL,
    mail_type character varying(20) NOT NULL,
    subject character varying(255) NOT NULL,
    description text NOT NULL,
    date_received timestamp with time zone,
    date_sent timestamp with time zone,
    priority character varying(20) NOT NULL,
    confidential boolean NOT NULL,
    file_number character varying(100) NOT NULL,
    delivery_method character varying(50) NOT NULL,
    weight numeric(10,2),
    postage_cost numeric(10,2),
    courier_name character varying(100) NOT NULL,
    courier_tracking_number character varying(100) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    sender_name character varying(255) NOT NULL,
    sender_address text NOT NULL,
    sender_phone character varying(50) NOT NULL,
    recipient_name character varying(255) NOT NULL,
    recipient_address text NOT NULL,
    recipient_phone character varying(50) NOT NULL,
    requires_response boolean NOT NULL,
    response_deadline date,
    created_by_id bigint NOT NULL,
    department_id bigint NOT NULL,
    response_mail_id bigint
);


ALTER TABLE public.mail_physicalmail OWNER TO dspop_user;

--
-- Name: mail_physicalmail_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.mail_physicalmail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mail_physicalmail_id_seq OWNER TO dspop_user;

--
-- Name: mail_physicalmail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.mail_physicalmail_id_seq OWNED BY public.mail_physicalmail.id;


--
-- Name: meetings_meeting; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.meetings_meeting (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    meeting_type_id bigint NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone,
    meeting_mode character varying(20) NOT NULL,
    physical_location character varying(255),
    virtual_meeting_url character varying(200),
    virtual_meeting_id character varying(100),
    virtual_meeting_password character varying(50),
    virtual_platform character varying(50),
    agenda text NOT NULL,
    minutes text,
    status character varying(20) NOT NULL,
    recording_url character varying(200),
    has_recording boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    department_id bigint NOT NULL,
    organizer_id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    content_type_id integer,
    object_id integer,
    CONSTRAINT meetings_meeting_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.meetings_meeting OWNER TO dspop_user;

--
-- Name: meetings_meeting_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.meetings_meeting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetings_meeting_id_seq OWNER TO dspop_user;

--
-- Name: meetings_meeting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.meetings_meeting_id_seq OWNED BY public.meetings_meeting.id;


--
-- Name: meetings_meetingaction; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.meetings_meetingaction (
    id bigint NOT NULL,
    description text NOT NULL,
    due_date date NOT NULL,
    assigned_to_id bigint NOT NULL,
    meeting_id bigint NOT NULL
);


ALTER TABLE public.meetings_meetingaction OWNER TO dspop_user;

--
-- Name: meetings_meetingaction_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.meetings_meetingaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetings_meetingaction_id_seq OWNER TO dspop_user;

--
-- Name: meetings_meetingaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.meetings_meetingaction_id_seq OWNED BY public.meetings_meetingaction.id;


--
-- Name: meetings_meetingdocument; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.meetings_meetingdocument (
    id bigint NOT NULL,
    document_type character varying(20) NOT NULL,
    notes text NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    document_id bigint NOT NULL,
    meeting_id bigint NOT NULL
);


ALTER TABLE public.meetings_meetingdocument OWNER TO dspop_user;

--
-- Name: meetings_meetingdocument_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.meetings_meetingdocument_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetings_meetingdocument_id_seq OWNER TO dspop_user;

--
-- Name: meetings_meetingdocument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.meetings_meetingdocument_id_seq OWNED BY public.meetings_meetingdocument.id;


--
-- Name: meetings_meetingparticipant; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.meetings_meetingparticipant (
    id bigint NOT NULL,
    role character varying(20) NOT NULL,
    meeting_id bigint NOT NULL,
    participant_id bigint,
    email character varying(254) NOT NULL,
    is_external boolean NOT NULL,
    mobile character varying(20) NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.meetings_meetingparticipant OWNER TO dspop_user;

--
-- Name: meetings_meetingparticipant_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.meetings_meetingparticipant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetings_meetingparticipant_id_seq OWNER TO dspop_user;

--
-- Name: meetings_meetingparticipant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.meetings_meetingparticipant_id_seq OWNED BY public.meetings_meetingparticipant.id;


--
-- Name: meetings_meetingtype; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.meetings_meetingtype (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.meetings_meetingtype OWNER TO dspop_user;

--
-- Name: meetings_meetingtype_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.meetings_meetingtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetings_meetingtype_id_seq OWNER TO dspop_user;

--
-- Name: meetings_meetingtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.meetings_meetingtype_id_seq OWNED BY public.meetings_meetingtype.id;


--
-- Name: memos_memo; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memo (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    reference_number character varying(100) NOT NULL,
    memo_type character varying(50) NOT NULL,
    content text NOT NULL,
    status character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    published_at timestamp with time zone,
    version_number integer NOT NULL,
    is_confidential boolean NOT NULL,
    external_recipient character varying(255),
    external_organization character varying(255),
    tags character varying(500) NOT NULL,
    file_number character varying(100) NOT NULL,
    created_by_id bigint NOT NULL,
    department_id bigint NOT NULL,
    document_id bigint,
    template_id bigint,
    content_type_id integer,
    object_id integer,
    CONSTRAINT memos_memo_object_id_check CHECK ((object_id >= 0)),
    CONSTRAINT memos_memo_version_number_check CHECK ((version_number >= 0))
);


ALTER TABLE public.memos_memo OWNER TO dspop_user;

--
-- Name: memos_memo_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memo_id_seq OWNER TO dspop_user;

--
-- Name: memos_memo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memo_id_seq OWNED BY public.memos_memo.id;


--
-- Name: memos_memo_recipient_departments; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memo_recipient_departments (
    id bigint NOT NULL,
    memo_id bigint NOT NULL,
    department_id bigint NOT NULL
);


ALTER TABLE public.memos_memo_recipient_departments OWNER TO dspop_user;

--
-- Name: memos_memo_recipient_departments_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memo_recipient_departments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memo_recipient_departments_id_seq OWNER TO dspop_user;

--
-- Name: memos_memo_recipient_departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memo_recipient_departments_id_seq OWNED BY public.memos_memo_recipient_departments.id;


--
-- Name: memos_memo_recipient_users; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memo_recipient_users (
    id bigint NOT NULL,
    memo_id bigint NOT NULL,
    customuser_id bigint NOT NULL
);


ALTER TABLE public.memos_memo_recipient_users OWNER TO dspop_user;

--
-- Name: memos_memo_recipient_users_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memo_recipient_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memo_recipient_users_id_seq OWNER TO dspop_user;

--
-- Name: memos_memo_recipient_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memo_recipient_users_id_seq OWNED BY public.memos_memo_recipient_users.id;


--
-- Name: memos_memoactivity; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memoactivity (
    id bigint NOT NULL,
    action character varying(20) NOT NULL,
    action_details jsonb,
    "timestamp" timestamp with time zone NOT NULL,
    ip_address inet,
    user_agent character varying(500) NOT NULL,
    document_id bigint,
    memo_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.memos_memoactivity OWNER TO dspop_user;

--
-- Name: memos_memoactivity_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memoactivity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memoactivity_id_seq OWNER TO dspop_user;

--
-- Name: memos_memoactivity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memoactivity_id_seq OWNED BY public.memos_memoactivity.id;


--
-- Name: memos_memoapproval; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memoapproval (
    id bigint NOT NULL,
    status character varying(20) NOT NULL,
    comments text NOT NULL,
    approved_at timestamp with time zone,
    level integer NOT NULL,
    approver_id bigint NOT NULL,
    memo_id bigint NOT NULL,
    signature_document_id bigint,
    CONSTRAINT memos_memoapproval_level_check CHECK ((level >= 0))
);


ALTER TABLE public.memos_memoapproval OWNER TO dspop_user;

--
-- Name: memos_memoapproval_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memoapproval_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memoapproval_id_seq OWNER TO dspop_user;

--
-- Name: memos_memoapproval_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memoapproval_id_seq OWNED BY public.memos_memoapproval.id;


--
-- Name: memos_memocomment; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memocomment (
    id bigint NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_internal boolean NOT NULL,
    memo_id bigint NOT NULL,
    parent_id bigint,
    user_id bigint NOT NULL
);


ALTER TABLE public.memos_memocomment OWNER TO dspop_user;

--
-- Name: memos_memocomment_attachments; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memocomment_attachments (
    id bigint NOT NULL,
    memocomment_id bigint NOT NULL,
    document_id bigint NOT NULL
);


ALTER TABLE public.memos_memocomment_attachments OWNER TO dspop_user;

--
-- Name: memos_memocomment_attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memocomment_attachments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memocomment_attachments_id_seq OWNER TO dspop_user;

--
-- Name: memos_memocomment_attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memocomment_attachments_id_seq OWNED BY public.memos_memocomment_attachments.id;


--
-- Name: memos_memocomment_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memocomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memocomment_id_seq OWNER TO dspop_user;

--
-- Name: memos_memocomment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memocomment_id_seq OWNED BY public.memos_memocomment.id;


--
-- Name: memos_memotemplate; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memotemplate (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    description text NOT NULL,
    content text NOT NULL,
    memo_type character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    created_by_id bigint NOT NULL,
    department_id bigint NOT NULL
);


ALTER TABLE public.memos_memotemplate OWNER TO dspop_user;

--
-- Name: memos_memotemplate_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memotemplate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memotemplate_id_seq OWNER TO dspop_user;

--
-- Name: memos_memotemplate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memotemplate_id_seq OWNED BY public.memos_memotemplate.id;


--
-- Name: memos_memoversion; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.memos_memoversion (
    id bigint NOT NULL,
    version_number integer NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    comments text NOT NULL,
    created_by_id bigint NOT NULL,
    document_id bigint,
    memo_id bigint NOT NULL,
    CONSTRAINT memos_memoversion_version_number_check CHECK ((version_number >= 0))
);


ALTER TABLE public.memos_memoversion OWNER TO dspop_user;

--
-- Name: memos_memoversion_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.memos_memoversion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.memos_memoversion_id_seq OWNER TO dspop_user;

--
-- Name: memos_memoversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.memos_memoversion_id_seq OWNED BY public.memos_memoversion.id;


--
-- Name: organization_department; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.organization_department (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    email character varying(254) NOT NULL
);


ALTER TABLE public.organization_department OWNER TO dspop_user;

--
-- Name: organization_department_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.organization_department_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_department_id_seq OWNER TO dspop_user;

--
-- Name: organization_department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.organization_department_id_seq OWNED BY public.organization_department.id;


--
-- Name: organization_role; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.organization_role (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    job_group character varying(4) NOT NULL,
    description text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    department_id bigint NOT NULL
);


ALTER TABLE public.organization_role OWNER TO dspop_user;

--
-- Name: organization_role_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.organization_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_role_id_seq OWNER TO dspop_user;

--
-- Name: organization_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.organization_role_id_seq OWNED BY public.organization_role.id;


--
-- Name: organization_role_permissions; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.organization_role_permissions (
    id bigint NOT NULL,
    role_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.organization_role_permissions OWNER TO dspop_user;

--
-- Name: organization_role_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.organization_role_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_role_permissions_id_seq OWNER TO dspop_user;

--
-- Name: organization_role_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.organization_role_permissions_id_seq OWNED BY public.organization_role_permissions.id;


--
-- Name: organization_userrole; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.organization_userrole (
    id bigint NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    role_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.organization_userrole OWNER TO dspop_user;

--
-- Name: organization_userrole_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.organization_userrole_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_userrole_id_seq OWNER TO dspop_user;

--
-- Name: organization_userrole_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.organization_userrole_id_seq OWNED BY public.organization_userrole.id;


--
-- Name: pmmu_financialyearperformance; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.pmmu_financialyearperformance (
    id bigint NOT NULL,
    target character varying(100) NOT NULL,
    baseline character varying(100),
    actual character varying(100),
    financial_year_id bigint NOT NULL,
    indicator_id bigint NOT NULL
);


ALTER TABLE public.pmmu_financialyearperformance OWNER TO dspop_user;

--
-- Name: pmmu_financialyearperformance_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.pmmu_financialyearperformance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pmmu_financialyearperformance_id_seq OWNER TO dspop_user;

--
-- Name: pmmu_financialyearperformance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.pmmu_financialyearperformance_id_seq OWNED BY public.pmmu_financialyearperformance.id;


--
-- Name: pmmu_indicatorcategory; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.pmmu_indicatorcategory (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    display_name character varying(255) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.pmmu_indicatorcategory OWNER TO dspop_user;

--
-- Name: pmmu_indicatorcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.pmmu_indicatorcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pmmu_indicatorcategory_id_seq OWNER TO dspop_user;

--
-- Name: pmmu_indicatorcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.pmmu_indicatorcategory_id_seq OWNED BY public.pmmu_indicatorcategory.id;


--
-- Name: pmmu_indicatornote; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.pmmu_indicatornote (
    id bigint NOT NULL,
    note_text text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by_id bigint,
    indicator_id bigint NOT NULL
);


ALTER TABLE public.pmmu_indicatornote OWNER TO dspop_user;

--
-- Name: pmmu_indicatornote_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.pmmu_indicatornote_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pmmu_indicatornote_id_seq OWNER TO dspop_user;

--
-- Name: pmmu_indicatornote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.pmmu_indicatornote_id_seq OWNED BY public.pmmu_indicatornote.id;


--
-- Name: pmmu_performanceindicator; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.pmmu_performanceindicator (
    id bigint NOT NULL,
    name text NOT NULL,
    unit_of_measure character varying(50) NOT NULL,
    weight integer NOT NULL,
    subcategory_id bigint,
    description text NOT NULL
);


ALTER TABLE public.pmmu_performanceindicator OWNER TO dspop_user;

--
-- Name: pmmu_performanceindicator_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.pmmu_performanceindicator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pmmu_performanceindicator_id_seq OWNER TO dspop_user;

--
-- Name: pmmu_performanceindicator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.pmmu_performanceindicator_id_seq OWNED BY public.pmmu_performanceindicator.id;


--
-- Name: pmmu_pmmu; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.pmmu_pmmu (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    financial_year_id bigint NOT NULL
);


ALTER TABLE public.pmmu_pmmu OWNER TO dspop_user;

--
-- Name: pmmu_pmmu_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.pmmu_pmmu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pmmu_pmmu_id_seq OWNER TO dspop_user;

--
-- Name: pmmu_pmmu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.pmmu_pmmu_id_seq OWNED BY public.pmmu_pmmu.id;


--
-- Name: statistics_adjournmentreason; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_adjournmentreason (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    unit_rank_id bigint NOT NULL
);


ALTER TABLE public.statistics_adjournmentreason OWNER TO dspop_user;

--
-- Name: statistics_adjournmentreason_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_adjournmentreason_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_adjournmentreason_id_seq OWNER TO dspop_user;

--
-- Name: statistics_adjournmentreason_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_adjournmentreason_id_seq OWNED BY public.statistics_adjournmentreason.id;


--
-- Name: statistics_caseactivitytype; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_caseactivitytype (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    unit_rank_id bigint NOT NULL
);


ALTER TABLE public.statistics_caseactivitytype OWNER TO dspop_user;

--
-- Name: statistics_caseactivitytype_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_caseactivitytype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_caseactivitytype_id_seq OWNER TO dspop_user;

--
-- Name: statistics_caseactivitytype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_caseactivitytype_id_seq OWNED BY public.statistics_caseactivitytype.id;


--
-- Name: statistics_casecategory; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_casecategory (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(10) NOT NULL,
    description text,
    unit_rank_id bigint NOT NULL
);


ALTER TABLE public.statistics_casecategory OWNER TO dspop_user;

--
-- Name: statistics_casecategory_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_casecategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_casecategory_id_seq OWNER TO dspop_user;

--
-- Name: statistics_casecategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_casecategory_id_seq OWNED BY public.statistics_casecategory.id;


--
-- Name: statistics_caseoutcome; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_caseoutcome (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    unit_rank_id bigint NOT NULL
);


ALTER TABLE public.statistics_caseoutcome OWNER TO dspop_user;

--
-- Name: statistics_caseoutcome_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_caseoutcome_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_caseoutcome_id_seq OWNER TO dspop_user;

--
-- Name: statistics_caseoutcome_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_caseoutcome_id_seq OWNED BY public.statistics_caseoutcome.id;


--
-- Name: statistics_dcrtdata; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_dcrtdata (
    id bigint NOT NULL,
    today_date_day integer,
    today_date_month character varying(255),
    today_date_year character varying(255),
    name_of_court character varying(255),
    case_number_number integer,
    case_number_day integer,
    case_number_month character varying(255),
    case_number_year integer,
    appeal_number_court_name character varying(255),
    appeal_number_code character varying(255),
    appeal_number_number integer,
    appeal_number_year integer,
    specific_case_type character varying(255),
    judicial_officer_1 character varying(255),
    judicial_officer_2 character varying(255),
    judicial_officer_3 character varying(255),
    judicial_officer_4 character varying(255),
    judicial_officer_5 character varying(255),
    judicial_officer_6 character varying(255),
    judicial_officer_7 character varying(255),
    judicial_officer_8 character varying(255),
    case_coming_for character varying(255),
    case_outcome character varying(255),
    adjournment_reason character varying(255),
    date_of_next_activity_day integer,
    date_of_next_activity_month character varying(255),
    date_of_next_activity_year integer,
    no_of_plaintiffs_or_appellants_male integer,
    no_of_plaintiffs_or_appellants_female integer,
    no_of_plaintiffs_or_appellants_organization integer,
    no_of_defendants_accused_male integer,
    no_of_defendants_accused_female integer,
    no_of_defendants_accused_organization integer,
    parties_have_legal_representation character varying(255),
    no_of_witnesses_in_court_d integer,
    no_of_witnesses_in_court_w integer,
    no_of_accused_remanded integer,
    last_date_of_submission_of_case_file_day character varying(255),
    last_date_of_submission_of_case_file_month character varying(255),
    last_date_of_submission_of_case_file_year character varying(255),
    remarks character varying(255),
    division_id bigint NOT NULL,
    financial_quarter_id bigint NOT NULL,
    financial_year_id bigint NOT NULL,
    month_id bigint NOT NULL,
    unit_id bigint NOT NULL,
    case_number_code_id bigint
);


ALTER TABLE public.statistics_dcrtdata OWNER TO dspop_user;

--
-- Name: statistics_dcrtdata_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_dcrtdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_dcrtdata_id_seq OWNER TO dspop_user;

--
-- Name: statistics_dcrtdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_dcrtdata_id_seq OWNED BY public.statistics_dcrtdata.id;


--
-- Name: statistics_division; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_division (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    code character varying(50) NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.statistics_division OWNER TO dspop_user;

--
-- Name: statistics_division_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_division_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_division_id_seq OWNER TO dspop_user;

--
-- Name: statistics_division_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_division_id_seq OWNED BY public.statistics_division.id;


--
-- Name: statistics_financialquarter; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_financialquarter (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    quarter_number integer NOT NULL,
    financial_year_id bigint NOT NULL
);


ALTER TABLE public.statistics_financialquarter OWNER TO dspop_user;

--
-- Name: statistics_financialquarter_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_financialquarter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_financialquarter_id_seq OWNER TO dspop_user;

--
-- Name: statistics_financialquarter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_financialquarter_id_seq OWNED BY public.statistics_financialquarter.id;


--
-- Name: statistics_financialyear; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_financialyear (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL
);


ALTER TABLE public.statistics_financialyear OWNER TO dspop_user;

--
-- Name: statistics_financialyear_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_financialyear_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_financialyear_id_seq OWNER TO dspop_user;

--
-- Name: statistics_financialyear_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_financialyear_id_seq OWNED BY public.statistics_financialyear.id;


--
-- Name: statistics_months; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_months (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    month_number integer NOT NULL,
    financial_quarter integer NOT NULL
);


ALTER TABLE public.statistics_months OWNER TO dspop_user;

--
-- Name: statistics_months_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_months_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_months_id_seq OWNER TO dspop_user;

--
-- Name: statistics_months_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_months_id_seq OWNED BY public.statistics_months.id;


--
-- Name: statistics_unit; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_unit (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    unique_id character varying(255) NOT NULL,
    unique_code character varying(255) NOT NULL,
    head_id_fk integer NOT NULL,
    subhead_id_fk integer NOT NULL,
    has_division boolean NOT NULL,
    is_court boolean NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    unit_rank_id bigint NOT NULL,
    is_template boolean NOT NULL,
    template_unit_id bigint,
    dcrt_unique_id character varying(255)
);


ALTER TABLE public.statistics_unit OWNER TO dspop_user;

--
-- Name: statistics_unit_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_unit_id_seq OWNER TO dspop_user;

--
-- Name: statistics_unit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_unit_id_seq OWNED BY public.statistics_unit.id;


--
-- Name: statistics_unitdivision; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_unitdivision (
    id bigint NOT NULL,
    division_id bigint NOT NULL,
    unit_id bigint NOT NULL
);


ALTER TABLE public.statistics_unitdivision OWNER TO dspop_user;

--
-- Name: statistics_unitdivision_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_unitdivision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_unitdivision_id_seq OWNER TO dspop_user;

--
-- Name: statistics_unitdivision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_unitdivision_id_seq OWNED BY public.statistics_unitdivision.id;


--
-- Name: statistics_unitrank; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.statistics_unitrank (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    is_court boolean NOT NULL
);


ALTER TABLE public.statistics_unitrank OWNER TO dspop_user;

--
-- Name: statistics_unitrank_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.statistics_unitrank_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_unitrank_id_seq OWNER TO dspop_user;

--
-- Name: statistics_unitrank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.statistics_unitrank_id_seq OWNED BY public.statistics_unitrank.id;


--
-- Name: tasks_comment; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.tasks_comment (
    id bigint NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    author_id bigint NOT NULL,
    task_id bigint NOT NULL
);


ALTER TABLE public.tasks_comment OWNER TO dspop_user;

--
-- Name: tasks_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.tasks_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_comment_id_seq OWNER TO dspop_user;

--
-- Name: tasks_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.tasks_comment_id_seq OWNED BY public.tasks_comment.id;


--
-- Name: tasks_project; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.tasks_project (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    owner_id bigint,
    department_id bigint
);


ALTER TABLE public.tasks_project OWNER TO dspop_user;

--
-- Name: tasks_project_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.tasks_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_project_id_seq OWNER TO dspop_user;

--
-- Name: tasks_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.tasks_project_id_seq OWNED BY public.tasks_project.id;


--
-- Name: tasks_task; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.tasks_task (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    priority integer NOT NULL,
    due_date date,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    creator_id bigint,
    project_id bigint NOT NULL,
    start_date date,
    parent_task_id bigint,
    content_type_id integer,
    object_id integer,
    CONSTRAINT tasks_task_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.tasks_task OWNER TO dspop_user;

--
-- Name: tasks_task_assignees; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.tasks_task_assignees (
    id bigint NOT NULL,
    task_id bigint NOT NULL,
    customuser_id bigint NOT NULL
);


ALTER TABLE public.tasks_task_assignees OWNER TO dspop_user;

--
-- Name: tasks_task_assignees_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.tasks_task_assignees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_assignees_id_seq OWNER TO dspop_user;

--
-- Name: tasks_task_assignees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.tasks_task_assignees_id_seq OWNED BY public.tasks_task_assignees.id;


--
-- Name: tasks_task_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.tasks_task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_id_seq OWNER TO dspop_user;

--
-- Name: tasks_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks_task.id;


--
-- Name: tasks_taskhistory; Type: TABLE; Schema: public; Owner: dspop_user
--

CREATE TABLE public.tasks_taskhistory (
    id bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    comment text,
    task_id bigint NOT NULL,
    user_id bigint,
    task_state jsonb NOT NULL,
    change_description character varying(255) NOT NULL
);


ALTER TABLE public.tasks_taskhistory OWNER TO dspop_user;

--
-- Name: tasks_taskhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: dspop_user
--

CREATE SEQUENCE public.tasks_taskhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_taskhistory_id_seq OWNER TO dspop_user;

--
-- Name: tasks_taskhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dspop_user
--

ALTER SEQUENCE public.tasks_taskhistory_id_seq OWNED BY public.tasks_taskhistory.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: authentication_customuser id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser ALTER COLUMN id SET DEFAULT nextval('public.authentication_customuser_id_seq'::regclass);


--
-- Name: authentication_customuser_departments id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_departments ALTER COLUMN id SET DEFAULT nextval('public.authentication_customuser_departments_id_seq'::regclass);


--
-- Name: authentication_customuser_groups id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_groups ALTER COLUMN id SET DEFAULT nextval('public.authentication_customuser_groups_id_seq'::regclass);


--
-- Name: authentication_customuser_user_permissions id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.authentication_customuser_user_permissions_id_seq'::regclass);


--
-- Name: budget_budgetcategory id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_budgetcategory ALTER COLUMN id SET DEFAULT nextval('public.budget_budgetcategory_id_seq'::regclass);


--
-- Name: budget_financialyear id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_financialyear ALTER COLUMN id SET DEFAULT nextval('public.budget_financialyear_id_seq'::regclass);


--
-- Name: budget_performanceindicator id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_performanceindicator ALTER COLUMN id SET DEFAULT nextval('public.budget_performanceindicator_id_seq'::regclass);


--
-- Name: budget_quarterlyallocation id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_quarterlyallocation ALTER COLUMN id SET DEFAULT nextval('public.budget_quarterlyallocation_id_seq'::regclass);


--
-- Name: budget_transformativeinitiative id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_transformativeinitiative ALTER COLUMN id SET DEFAULT nextval('public.budget_transformativeinitiative_id_seq'::regclass);


--
-- Name: budget_workplanitem id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_workplanitem ALTER COLUMN id SET DEFAULT nextval('public.budget_workplanitem_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: document_management_document id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_document ALTER COLUMN id SET DEFAULT nextval('public.document_management_document_id_seq'::regclass);


--
-- Name: document_management_documentaccess id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentaccess ALTER COLUMN id SET DEFAULT nextval('public.document_management_documentaccess_id_seq'::regclass);


--
-- Name: document_management_documentactivity id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentactivity ALTER COLUMN id SET DEFAULT nextval('public.document_management_documentactivity_id_seq'::regclass);


--
-- Name: document_management_documentcategory id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcategory ALTER COLUMN id SET DEFAULT nextval('public.document_management_documentcategory_id_seq'::regclass);


--
-- Name: document_management_documentcomment id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcomment ALTER COLUMN id SET DEFAULT nextval('public.document_management_documentcomment_id_seq'::regclass);


--
-- Name: home_module id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module ALTER COLUMN id SET DEFAULT nextval('public.home_module_id_seq'::regclass);


--
-- Name: home_module_departments id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module_departments ALTER COLUMN id SET DEFAULT nextval('public.home_module_departments_id_seq'::regclass);


--
-- Name: innovations_innovation id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovation ALTER COLUMN id SET DEFAULT nextval('public.innovations_innovation_id_seq'::regclass);


--
-- Name: innovations_innovationattachment id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovationattachment ALTER COLUMN id SET DEFAULT nextval('public.innovations_innovationattachment_id_seq'::regclass);


--
-- Name: mail_mailactivity id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailactivity ALTER COLUMN id SET DEFAULT nextval('public.mail_mailactivity_id_seq'::regclass);


--
-- Name: mail_mailassignment id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailassignment ALTER COLUMN id SET DEFAULT nextval('public.mail_mailassignment_id_seq'::regclass);


--
-- Name: mail_mailattachment id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailattachment ALTER COLUMN id SET DEFAULT nextval('public.mail_mailattachment_id_seq'::regclass);


--
-- Name: mail_mailmovement id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailmovement ALTER COLUMN id SET DEFAULT nextval('public.mail_mailmovement_id_seq'::regclass);


--
-- Name: mail_physicalmail id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_physicalmail ALTER COLUMN id SET DEFAULT nextval('public.mail_physicalmail_id_seq'::regclass);


--
-- Name: meetings_meeting id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting ALTER COLUMN id SET DEFAULT nextval('public.meetings_meeting_id_seq'::regclass);


--
-- Name: meetings_meetingaction id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingaction ALTER COLUMN id SET DEFAULT nextval('public.meetings_meetingaction_id_seq'::regclass);


--
-- Name: meetings_meetingdocument id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingdocument ALTER COLUMN id SET DEFAULT nextval('public.meetings_meetingdocument_id_seq'::regclass);


--
-- Name: meetings_meetingparticipant id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingparticipant ALTER COLUMN id SET DEFAULT nextval('public.meetings_meetingparticipant_id_seq'::regclass);


--
-- Name: meetings_meetingtype id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingtype ALTER COLUMN id SET DEFAULT nextval('public.meetings_meetingtype_id_seq'::regclass);


--
-- Name: memos_memo id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo ALTER COLUMN id SET DEFAULT nextval('public.memos_memo_id_seq'::regclass);


--
-- Name: memos_memo_recipient_departments id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_departments ALTER COLUMN id SET DEFAULT nextval('public.memos_memo_recipient_departments_id_seq'::regclass);


--
-- Name: memos_memo_recipient_users id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_users ALTER COLUMN id SET DEFAULT nextval('public.memos_memo_recipient_users_id_seq'::regclass);


--
-- Name: memos_memoactivity id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoactivity ALTER COLUMN id SET DEFAULT nextval('public.memos_memoactivity_id_seq'::regclass);


--
-- Name: memos_memoapproval id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoapproval ALTER COLUMN id SET DEFAULT nextval('public.memos_memoapproval_id_seq'::regclass);


--
-- Name: memos_memocomment id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment ALTER COLUMN id SET DEFAULT nextval('public.memos_memocomment_id_seq'::regclass);


--
-- Name: memos_memocomment_attachments id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment_attachments ALTER COLUMN id SET DEFAULT nextval('public.memos_memocomment_attachments_id_seq'::regclass);


--
-- Name: memos_memotemplate id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memotemplate ALTER COLUMN id SET DEFAULT nextval('public.memos_memotemplate_id_seq'::regclass);


--
-- Name: memos_memoversion id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoversion ALTER COLUMN id SET DEFAULT nextval('public.memos_memoversion_id_seq'::regclass);


--
-- Name: organization_department id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_department ALTER COLUMN id SET DEFAULT nextval('public.organization_department_id_seq'::regclass);


--
-- Name: organization_role id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role ALTER COLUMN id SET DEFAULT nextval('public.organization_role_id_seq'::regclass);


--
-- Name: organization_role_permissions id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role_permissions ALTER COLUMN id SET DEFAULT nextval('public.organization_role_permissions_id_seq'::regclass);


--
-- Name: organization_userrole id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_userrole ALTER COLUMN id SET DEFAULT nextval('public.organization_userrole_id_seq'::regclass);


--
-- Name: pmmu_financialyearperformance id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_financialyearperformance ALTER COLUMN id SET DEFAULT nextval('public.pmmu_financialyearperformance_id_seq'::regclass);


--
-- Name: pmmu_indicatorcategory id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatorcategory ALTER COLUMN id SET DEFAULT nextval('public.pmmu_indicatorcategory_id_seq'::regclass);


--
-- Name: pmmu_indicatornote id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatornote ALTER COLUMN id SET DEFAULT nextval('public.pmmu_indicatornote_id_seq'::regclass);


--
-- Name: pmmu_performanceindicator id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_performanceindicator ALTER COLUMN id SET DEFAULT nextval('public.pmmu_performanceindicator_id_seq'::regclass);


--
-- Name: pmmu_pmmu id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_pmmu ALTER COLUMN id SET DEFAULT nextval('public.pmmu_pmmu_id_seq'::regclass);


--
-- Name: statistics_adjournmentreason id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_adjournmentreason ALTER COLUMN id SET DEFAULT nextval('public.statistics_adjournmentreason_id_seq'::regclass);


--
-- Name: statistics_caseactivitytype id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseactivitytype ALTER COLUMN id SET DEFAULT nextval('public.statistics_caseactivitytype_id_seq'::regclass);


--
-- Name: statistics_casecategory id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_casecategory ALTER COLUMN id SET DEFAULT nextval('public.statistics_casecategory_id_seq'::regclass);


--
-- Name: statistics_caseoutcome id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseoutcome ALTER COLUMN id SET DEFAULT nextval('public.statistics_caseoutcome_id_seq'::regclass);


--
-- Name: statistics_dcrtdata id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata ALTER COLUMN id SET DEFAULT nextval('public.statistics_dcrtdata_id_seq'::regclass);


--
-- Name: statistics_division id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_division ALTER COLUMN id SET DEFAULT nextval('public.statistics_division_id_seq'::regclass);


--
-- Name: statistics_financialquarter id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_financialquarter ALTER COLUMN id SET DEFAULT nextval('public.statistics_financialquarter_id_seq'::regclass);


--
-- Name: statistics_financialyear id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_financialyear ALTER COLUMN id SET DEFAULT nextval('public.statistics_financialyear_id_seq'::regclass);


--
-- Name: statistics_months id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_months ALTER COLUMN id SET DEFAULT nextval('public.statistics_months_id_seq'::regclass);


--
-- Name: statistics_unit id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unit ALTER COLUMN id SET DEFAULT nextval('public.statistics_unit_id_seq'::regclass);


--
-- Name: statistics_unitdivision id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unitdivision ALTER COLUMN id SET DEFAULT nextval('public.statistics_unitdivision_id_seq'::regclass);


--
-- Name: statistics_unitrank id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unitrank ALTER COLUMN id SET DEFAULT nextval('public.statistics_unitrank_id_seq'::regclass);


--
-- Name: tasks_comment id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_comment ALTER COLUMN id SET DEFAULT nextval('public.tasks_comment_id_seq'::regclass);


--
-- Name: tasks_project id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_project ALTER COLUMN id SET DEFAULT nextval('public.tasks_project_id_seq'::regclass);


--
-- Name: tasks_task id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);


--
-- Name: tasks_task_assignees id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task_assignees ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_assignees_id_seq'::regclass);


--
-- Name: tasks_taskhistory id; Type: DEFAULT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_taskhistory ALTER COLUMN id SET DEFAULT nextval('public.tasks_taskhistory_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_customuser
22	Can change user	6	change_customuser
23	Can delete user	6	delete_customuser
24	Can view user	6	view_customuser
25	Can add module	7	add_module
26	Can change module	7	change_module
27	Can delete module	7	delete_module
28	Can view module	7	view_module
29	Can add division	8	add_division
30	Can change division	8	change_division
31	Can delete division	8	delete_division
32	Can view division	8	view_division
33	Can add financial year	9	add_financialyear
34	Can change financial year	9	change_financialyear
35	Can delete financial year	9	delete_financialyear
36	Can view financial year	9	view_financialyear
37	Can add months	10	add_months
38	Can change months	10	change_months
39	Can delete months	10	delete_months
40	Can view months	10	view_months
41	Can add unit	11	add_unit
42	Can change unit	11	change_unit
43	Can delete unit	11	delete_unit
44	Can view unit	11	view_unit
45	Can add unit rank	12	add_unitrank
46	Can change unit rank	12	change_unitrank
47	Can delete unit rank	12	delete_unitrank
48	Can view unit rank	12	view_unitrank
49	Can add unit division	13	add_unitdivision
50	Can change unit division	13	change_unitdivision
51	Can delete unit division	13	delete_unitdivision
52	Can view unit division	13	view_unitdivision
53	Can add financial quarter	14	add_financialquarter
54	Can change financial quarter	14	change_financialquarter
55	Can delete financial quarter	14	delete_financialquarter
56	Can view financial quarter	14	view_financialquarter
57	Can add dcrt data	15	add_dcrtdata
58	Can change dcrt data	15	change_dcrtdata
59	Can delete dcrt data	15	delete_dcrtdata
60	Can view dcrt data	15	view_dcrtdata
61	Can add case activity type	16	add_caseactivitytype
62	Can change case activity type	16	change_caseactivitytype
63	Can delete case activity type	16	delete_caseactivitytype
64	Can view case activity type	16	view_caseactivitytype
65	Can add case category	17	add_casecategory
66	Can change case category	17	change_casecategory
67	Can delete case category	17	delete_casecategory
68	Can view case category	17	view_casecategory
69	Can add case outcome	18	add_caseoutcome
70	Can change case outcome	18	change_caseoutcome
71	Can delete case outcome	18	delete_caseoutcome
72	Can view case outcome	18	view_caseoutcome
73	Can add adjournment reason	19	add_adjournmentreason
74	Can change adjournment reason	19	change_adjournmentreason
75	Can delete adjournment reason	19	delete_adjournmentreason
76	Can view adjournment reason	19	view_adjournmentreason
77	Can add document	20	add_document
78	Can change document	20	change_document
79	Can delete document	20	delete_document
80	Can view document	20	view_document
81	Can add document category	21	add_documentcategory
82	Can change document category	21	change_documentcategory
83	Can delete document category	21	delete_documentcategory
84	Can view document category	21	view_documentcategory
85	Can add document activity	22	add_documentactivity
86	Can change document activity	22	change_documentactivity
87	Can delete document activity	22	delete_documentactivity
88	Can view document activity	22	view_documentactivity
89	Can add document access	23	add_documentaccess
90	Can change document access	23	change_documentaccess
91	Can delete document access	23	delete_documentaccess
92	Can view document access	23	view_documentaccess
93	Can add department	24	add_department
94	Can change department	24	change_department
95	Can delete department	24	delete_department
96	Can view department	24	view_department
97	Can add role	25	add_role
98	Can change role	25	change_role
99	Can delete role	25	delete_role
100	Can view role	25	view_role
101	Can add user role	26	add_userrole
102	Can change user role	26	change_userrole
103	Can delete user role	26	delete_userrole
104	Can view user role	26	view_userrole
105	Can add budget category	27	add_budgetcategory
106	Can change budget category	27	change_budgetcategory
107	Can delete budget category	27	delete_budgetcategory
108	Can view budget category	27	view_budgetcategory
109	Can add financial year	28	add_financialyear
110	Can change financial year	28	change_financialyear
111	Can delete financial year	28	delete_financialyear
112	Can view financial year	28	view_financialyear
113	Can add workplan item	29	add_workplanitem
114	Can change workplan item	29	change_workplanitem
115	Can delete workplan item	29	delete_workplanitem
116	Can view workplan item	29	view_workplanitem
117	Can add transformative initiative	30	add_transformativeinitiative
118	Can change transformative initiative	30	change_transformativeinitiative
119	Can delete transformative initiative	30	delete_transformativeinitiative
120	Can view transformative initiative	30	view_transformativeinitiative
121	Can add performance indicator	31	add_performanceindicator
122	Can change performance indicator	31	change_performanceindicator
123	Can delete performance indicator	31	delete_performanceindicator
124	Can view performance indicator	31	view_performanceindicator
125	Can add quarterly allocation	32	add_quarterlyallocation
126	Can change quarterly allocation	32	change_quarterlyallocation
127	Can delete quarterly allocation	32	delete_quarterlyallocation
128	Can view quarterly allocation	32	view_quarterlyallocation
129	Can add meeting	33	add_meeting
130	Can change meeting	33	change_meeting
131	Can delete meeting	33	delete_meeting
132	Can view meeting	33	view_meeting
133	Can view all meetings across departments	33	view_all_meetings
134	Can manage department meetings	33	manage_department_meetings
135	Can add Meeting Participant	34	add_meetingparticipant
136	Can change Meeting Participant	34	change_meetingparticipant
137	Can delete Meeting Participant	34	delete_meetingparticipant
138	Can view Meeting Participant	34	view_meetingparticipant
139	Can add Meeting Action Item	35	add_meetingaction
140	Can change Meeting Action Item	35	change_meetingaction
141	Can delete Meeting Action Item	35	delete_meetingaction
142	Can view Meeting Action Item	35	view_meetingaction
143	Can add Meeting Document	36	add_meetingdocument
144	Can change Meeting Document	36	change_meetingdocument
145	Can delete Meeting Document	36	delete_meetingdocument
146	Can view Meeting Document	36	view_meetingdocument
147	Can add meeting type	37	add_meetingtype
148	Can change meeting type	37	change_meetingtype
149	Can delete meeting type	37	delete_meetingtype
150	Can view meeting type	37	view_meetingtype
151	Can add innovation	38	add_innovation
152	Can change innovation	38	change_innovation
153	Can delete innovation	38	delete_innovation
154	Can view innovation	38	view_innovation
155	Can view all innovations	38	view_all_innovations
156	Can approve innovation	38	approve_innovation
157	Can reject innovation	38	reject_innovation
158	Can view innovation	38	can_view_innovation
159	Can change innovation	38	can_change_innovation
160	Can delete innovation	38	can_delete_innovation
161	Can add innovation attachment	39	add_innovationattachment
162	Can change innovation attachment	39	change_innovationattachment
163	Can delete innovation attachment	39	delete_innovationattachment
164	Can view innovation attachment	39	view_innovationattachment
165	Can add memo	40	add_memo
166	Can change memo	40	change_memo
167	Can delete memo	40	delete_memo
168	Can view memo	40	view_memo
169	Can approve memos	40	can_approve_memos
170	Can publish memos	40	can_publish_memos
171	Can view department memos	40	view_department_memos
172	Can add memo template	41	add_memotemplate
173	Can change memo template	41	change_memotemplate
174	Can delete memo template	41	delete_memotemplate
175	Can view memo template	41	view_memotemplate
176	Can add memo comment	42	add_memocomment
177	Can change memo comment	42	change_memocomment
178	Can delete memo comment	42	delete_memocomment
179	Can view memo comment	42	view_memocomment
180	Can add memo activity	43	add_memoactivity
181	Can change memo activity	43	change_memoactivity
182	Can delete memo activity	43	delete_memoactivity
183	Can view memo activity	43	view_memoactivity
184	Can add memo version	44	add_memoversion
185	Can change memo version	44	change_memoversion
186	Can delete memo version	44	delete_memoversion
187	Can view memo version	44	view_memoversion
188	Can add memo approval	45	add_memoapproval
189	Can change memo approval	45	change_memoapproval
190	Can delete memo approval	45	delete_memoapproval
191	Can view memo approval	45	view_memoapproval
192	Can add physical mail	46	add_physicalmail
193	Can change physical mail	46	change_physicalmail
194	Can delete physical mail	46	delete_physicalmail
195	Can view physical mail	46	view_physicalmail
196	Can mark mail as confidential	46	can_mark_confidential
197	Can view confidential mail	46	view_confidential_mail
198	Can process incoming mail	46	process_incoming_mail
199	Can dispatch outgoing mail	46	dispatch_outgoing_mail
200	Can add mail movement	47	add_mailmovement
201	Can change mail movement	47	change_mailmovement
202	Can delete mail movement	47	delete_mailmovement
203	Can view mail movement	47	view_mailmovement
204	Can add mail attachment	48	add_mailattachment
205	Can change mail attachment	48	change_mailattachment
206	Can delete mail attachment	48	delete_mailattachment
207	Can view mail attachment	48	view_mailattachment
208	Can add mail assignment	49	add_mailassignment
209	Can change mail assignment	49	change_mailassignment
210	Can delete mail assignment	49	delete_mailassignment
211	Can view mail assignment	49	view_mailassignment
212	Can add mail activity	50	add_mailactivity
213	Can change mail activity	50	change_mailactivity
214	Can delete mail activity	50	delete_mailactivity
215	Can view mail activity	50	view_mailactivity
216	Can add PMMU Understanding	51	add_pmmu
217	Can change PMMU Understanding	51	change_pmmu
218	Can delete PMMU Understanding	51	delete_pmmu
219	Can view PMMU Understanding	51	view_pmmu
220	Can add Indicator Note	52	add_indicatornote
221	Can change Indicator Note	52	change_indicatornote
222	Can delete Indicator Note	52	delete_indicatornote
223	Can view Indicator Note	52	view_indicatornote
224	Can add Indicator Category	53	add_indicatorcategory
225	Can change Indicator Category	53	change_indicatorcategory
226	Can delete Indicator Category	53	delete_indicatorcategory
227	Can view Indicator Category	53	view_indicatorcategory
228	Can add Performance Indicator	54	add_performanceindicator
229	Can change Performance Indicator	54	change_performanceindicator
230	Can delete Performance Indicator	54	delete_performanceindicator
231	Can view Performance Indicator	54	view_performanceindicator
232	Can add Financial Year Performance Data	55	add_financialyearperformance
233	Can change Financial Year Performance Data	55	change_financialyearperformance
234	Can delete Financial Year Performance Data	55	delete_financialyearperformance
235	Can view Financial Year Performance Data	55	view_financialyearperformance
236	Can add Project	56	add_project
237	Can change Project	56	change_project
238	Can delete Project	56	delete_project
239	Can view Project	56	view_project
240	Can add Task	57	add_task
241	Can change Task	57	change_task
242	Can delete Task	57	delete_task
243	Can view Task	57	view_task
244	Can add Comment	58	add_comment
245	Can change Comment	58	change_comment
246	Can delete Comment	58	delete_comment
247	Can view Comment	58	view_comment
248	Can add document comment	59	add_documentcomment
249	Can change document comment	59	change_documentcomment
250	Can delete document comment	59	delete_documentcomment
251	Can view document comment	59	view_documentcomment
252	Can add Task History	60	add_taskhistory
253	Can change Task History	60	change_taskhistory
254	Can delete Task History	60	delete_taskhistory
255	Can view Task History	60	view_taskhistory
\.


--
-- Data for Name: authentication_customuser; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.authentication_customuser (id, password, last_login, is_superuser, username, email, is_staff, is_active, date_joined, first_name, last_name, pj_number, phone, mobile) FROM stdin;
20	pbkdf2_sha256$260000$HwmJp4zpA87so8qsLrqCAd$YTVI+LlKLKstXKEdDDrPOvniEEPltcZ9UmhS2In6ZWE=	\N	f	lorna.barasa	lorna.barasa@judiciary.go.ke	t	t	2025-05-21 12:04:56.35025+00	Lorna	Barasa			
1	pbkdf2_sha256$260000$HaEfY5YZGHWcRxqMfQZyod$A1eGFPIpPqwCfl4AP6l9NbpQgtQwKj2KRIkaouJT+t0=	2025-07-02 11:09:06.542164+00	t	joseph.osewe	joseph.osewe@judiciary.go.ke	t	t	2025-05-19 12:19:23.877719+00					
6	pbkdf2_sha256$260000$J1hxudxFKdV67uKPkKETSK$d4IzVao/eTFW12hPxyCLNDod6Yl8XNf74zrwmSeTs/s=	\N	f	alex.njeru	alex.njeru@judiciary.go.ke	t	t	2025-05-21 12:04:52.283747+00	Alex	Njeru			
8	pbkdf2_sha256$260000$8MAlrjqQCYpzU00FwSUmh2$tcCwsMMFhbDap8i126zIh00qW17F/AzO8D/dTKWNRYY=	\N	f	steve.njehia	steve.njehia@judiciary.go.ke	t	t	2025-05-21 12:04:52.808771+00	Steve	Njehia			
9	pbkdf2_sha256$260000$2Ev6nEXEJQgOuWakBkeGhO$ejoU5JfmrNZMzF39KXQNdsqLbTc0MD6qg1sUiZctGEE=	\N	f	eugene.omondi	eugene.omondi@judiciary.go.ke	t	t	2025-05-21 12:04:53.144039+00	Eugene	Omondi			
14	pbkdf2_sha256$260000$es42QDELKTNUEawimpEiTk$1U9oG6K1/0KyhC42SD4X5nuDH0XgvUYZGKBhI13Zk9E=	2025-06-30 11:59:57.303801+00	f	john.mbiti	john.mbiti@court.go.ke	t	t	2025-05-21 12:04:54.50031+00	John	Mbiti			
12	pbkdf2_sha256$260000$gbtoUYQ4pDf8aVOwtIV4WR$LTmxre2WLltKMKhFboD1wrVymRySmOEkCwC58xppvyQ=	\N	f	linda.navakhole	linda.navakhole@judiciary.go.ke	t	t	2025-05-21 12:04:53.916939+00	Linda	Navakhole			
13	pbkdf2_sha256$260000$EkNL4zpzW3yGoN1hEQoxf5$gMpb/l/RH+N2l0Cv8MYbteU0hsVS8YBCaFMeLMBZfIk=	\N	f	melly.kiprop	melly.kiprop@judiciary.go.ke	t	t	2025-05-21 12:04:54.275475+00	Melly	Kiprop			
16	pbkdf2_sha256$260000$rZpnECQbWDGKaXsQZQO8ys$APDm5PuGYExoD4dep3BzeDOV/5DrsQvfbEzhIl9vaes=	\N	f	solomon.onaya	solomon.onaya@judiciary.go.ke	t	t	2025-05-21 12:04:55.166886+00	Solomon	Onaya			
17	pbkdf2_sha256$260000$coQTabH2b65ruKdA5cyZ1d$fZA1PBijk9o4S2gVbeX0PbNnHhn92Q4t9XUWbdkJLP0=	\N	f	yusuf.jarso	yusuf.jarso@judiciary.go.ke	t	t	2025-05-21 12:04:55.542057+00	Yusuf	Jarso			
18	pbkdf2_sha256$260000$oSYl1dATTQ66nweiGoSdfc$6yYanQv09K00U0ANBSN9lHtVJSbAs8eLB85VI6XIvQk=	\N	f	lucy.wangare	lucy.wangare@judiciary.go.ke	t	t	2025-05-21 12:04:55.766904+00	Lucy	Wangare			
19	pbkdf2_sha256$260000$7XadwkeAT396dkYkLfdFRZ$V0w4UPZCR25azRWI/X0RemAEJxhDAMeGXwhUEtlslDo=	\N	f	hannah.gichuru	hannah.gichuru@judiciary.go.ke	t	t	2025-05-21 12:04:56.117909+00	Hannah	Gichuru			
15	pbkdf2_sha256$260000$YqGKKVJ3IzcMaJkvGsAYhG$kElFYd3Ke+P4TBoeTML+4dRymOkYIRhNCwqSCVh2bAc=	\N	f	margaret.ochieng	margaret.ochieng@judiciary.go.ke	t	t	2025-05-21 12:04:54.925406+00	Margaret	Ochieng			
5	pbkdf2_sha256$260000$ekOWVy4l2FdWYA5qvEajIB$iCxdoIhVKL8zlMRV/WtOKtrm6+7ipibEqZg/WezTmIE=	\N	f	stanford.mwangi	stanford.mwangi@judiciary.go.ke	t	t	2025-05-21 12:04:52.009518+00	Stanford	Mwangi			
2	pbkdf2_sha256$260000$FSTNA8LRAd7rsirrXKmAoG$mXpWgmZ9zbKQlBeZxTj+XWBogh3fdMNAvYL75GQMzis=	\N	f	gilbert.kirui	gilbert.kirui@judiciary.go.ke	t	t	2025-05-21 12:04:24.129343+00	Gilbert	Kirui			
4	pbkdf2_sha256$260000$ZvlXvycPKV3Z984PvbVOsz$PVPfmECAAmoqx/CIHCqfTV3eGtRjimYJ2wvTuUHzRbo=	\N	f	dominic.nyambane	dominic.nyambane@judiciary.go.ke	t	t	2025-05-21 12:04:51.643243+00	Dominic	Nyambane			
11	pbkdf2_sha256$260000$jq3pV3JClZcRBD7VfOU18z$Qyf42Bhso9H25SrXDQ+Q9D0osmhcwrbyJ0KSQhuAofw=	\N	f	caroline.mungai	caroline.mungai@judiciary.go.ke	t	t	2025-05-21 12:04:53.700341+00	Caroline	Mungai			
21	pbkdf2_sha256$260000$VFyliCcDABpEPtlxxKPTvp$vYMnl+k8pdXKl8N6pr2OzaL1k0FS4D845YjNXJBe9ug=	2025-06-30 12:12:04.907728+00	t	pngobiro	pngobiro@gmail.com	t	t	2025-05-29 11:44:18.325152+00					
7	pbkdf2_sha256$260000$fmltRyy6iMHE1c3fazm4As$RzKOzVxaFn3+XFvjNw6Jkfo3WHc/o078diT3umB9OiA=	\N	f	erick.kocheli	erick.kocheli@judiciary.go.ke	t	t	2025-05-21 12:04:52.533665+00	Erick	Kocheli			
10	pbkdf2_sha256$260000$mbAsLbq3iWHndX25yJzsVG$R5qmk9YYdCHY/ANy/S2KFSBxqomI8ltH/NY9ZZuudeQ=	\N	f	martin.astiba	martin.astiba@judiciary.go.ke	t	t	2025-05-21 12:04:53.358947+00	Martin	Astiba			
3	pbkdf2_sha256$260000$UvOMpv9W5UoTn6XZUGUPCY$eVYw8LVTV9Jtrn703p/7DPZTaYR8qeRXJagLGPtwBKI=	\N	f	george.obai	george.obai@judiciary.go.ke	t	t	2025-05-21 12:04:51.386377+00	George	Obai			
\.


--
-- Data for Name: authentication_customuser_departments; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.authentication_customuser_departments (id, customuser_id, department_id) FROM stdin;
7	8	1
8	9	1
11	12	1
15	16	1
16	17	1
17	18	1
18	19	1
19	20	1
20	21	1
21	1	1
22	5	4
23	2	4
24	4	3
25	11	5
26	7	4
27	10	4
28	3	3
29	14	3
30	6	3
31	13	4
32	15	4
\.


--
-- Data for Name: authentication_customuser_groups; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.authentication_customuser_groups (id, customuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: authentication_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.authentication_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: budget_budgetcategory; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.budget_budgetcategory (id, name, code) FROM stdin;
\.


--
-- Data for Name: budget_financialyear; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.budget_financialyear (id, name, start_date, end_date) FROM stdin;
\.


--
-- Data for Name: budget_performanceindicator; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.budget_performanceindicator (id, name, description, baseline, target, measurement_frequency, workplan_item_id) FROM stdin;
\.


--
-- Data for Name: budget_quarterlyallocation; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.budget_quarterlyallocation (id, quarter, amount, workplan_item_id) FROM stdin;
\.


--
-- Data for Name: budget_transformativeinitiative; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.budget_transformativeinitiative (id, implementation_status, start_date, end_date, progress, workplan_item_id) FROM stdin;
\.


--
-- Data for Name: budget_workplanitem; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.budget_workplanitem (id, name, budget_code, description, item_type, total_amount, category_id, financial_year_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-05-20 13:39:13.794768+00	2	Meetings	2	[{"changed": {"fields": ["Departments"]}}]	7	1
2	2025-05-20 14:08:15.391312+00	4	Statistics	2	[{"changed": {"fields": ["Departments"]}}]	7	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	authentication	customuser
7	home	module
8	statistics	division
9	statistics	financialyear
10	statistics	months
11	statistics	unit
12	statistics	unitrank
13	statistics	unitdivision
14	statistics	financialquarter
15	statistics	dcrtdata
16	statistics	caseactivitytype
17	statistics	casecategory
18	statistics	caseoutcome
19	statistics	adjournmentreason
20	document_management	document
21	document_management	documentcategory
22	document_management	documentactivity
23	document_management	documentaccess
24	organization	department
25	organization	role
26	organization	userrole
27	budget	budgetcategory
28	budget	financialyear
29	budget	workplanitem
30	budget	transformativeinitiative
31	budget	performanceindicator
32	budget	quarterlyallocation
33	meetings	meeting
34	meetings	meetingparticipant
35	meetings	meetingaction
36	meetings	meetingdocument
37	meetings	meetingtype
38	innovations	innovation
39	innovations	innovationattachment
40	memos	memo
41	memos	memotemplate
42	memos	memocomment
43	memos	memoactivity
44	memos	memoversion
45	memos	memoapproval
46	mail	physicalmail
47	mail	mailmovement
48	mail	mailattachment
49	mail	mailassignment
50	mail	mailactivity
51	pmmu	pmmu
52	pmmu	indicatornote
53	pmmu	indicatorcategory
54	pmmu	performanceindicator
55	pmmu	financialyearperformance
56	tasks	project
57	tasks	task
58	tasks	comment
59	document_management	documentcomment
60	tasks	taskhistory
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-05-19 12:13:30.219753+00
2	authentication	0001_initial	2025-05-19 12:13:30.453571+00
3	admin	0001_initial	2025-05-19 12:13:30.870457+00
4	admin	0002_logentry_remove_auto_add	2025-05-19 12:13:30.92461+00
5	admin	0003_logentry_add_action_flag_choices	2025-05-19 12:13:30.94772+00
6	contenttypes	0002_remove_content_type_name	2025-05-19 12:13:31.112584+00
7	auth	0001_initial	2025-05-19 12:13:31.970725+00
8	auth	0002_alter_permission_name_max_length	2025-05-19 12:13:31.983708+00
9	auth	0003_alter_user_email_max_length	2025-05-19 12:13:31.998951+00
10	auth	0004_alter_user_username_opts	2025-05-19 12:13:32.009335+00
11	auth	0005_alter_user_last_login_null	2025-05-19 12:13:32.024842+00
12	auth	0006_require_contenttypes_0002	2025-05-19 12:13:32.028782+00
13	auth	0007_alter_validators_add_error_messages	2025-05-19 12:13:32.041796+00
14	auth	0008_alter_user_username_max_length	2025-05-19 12:13:32.049217+00
15	auth	0009_alter_user_last_name_max_length	2025-05-19 12:13:32.058951+00
16	auth	0010_alter_group_name_max_length	2025-05-19 12:13:32.077971+00
17	auth	0011_update_proxy_permissions	2025-05-19 12:13:32.093571+00
18	auth	0012_alter_user_first_name_max_length	2025-05-19 12:13:32.10804+00
19	organization	0001_initial	2025-05-19 12:13:32.613898+00
20	authentication	0002_initial	2025-05-19 12:13:33.430065+00
21	budget	0001_initial	2025-05-19 12:13:34.914312+00
22	document_management	0001_initial	2025-05-19 12:13:35.783805+00
23	organization	0002_role_permissions	2025-05-19 12:13:36.024961+00
24	home	0001_initial	2025-05-19 12:13:36.483762+00
25	home	0002_remove_module_department_module_departments	2025-05-19 12:13:36.892004+00
26	statistics	0001_initial	2025-05-19 12:13:38.392766+00
27	innovations	0001_initial	2025-05-19 12:13:39.193083+00
28	mail	0001_initial	2025-05-19 12:13:40.519739+00
29	meetings	0001_initial	2025-05-19 12:13:41.578233+00
30	meetings	0002_add_meeting_types	2025-05-19 12:13:41.927375+00
31	meetings	0003_populate_meeting_types	2025-05-19 12:13:42.090388+00
32	memos	0001_initial	2025-05-19 12:13:44.863925+00
33	pmmu	0001_initial	2025-05-19 12:13:45.831056+00
34	pmmu	0002_indicator_description	2025-05-19 12:13:45.871352+00
35	pmmu	0003_indicatorcategory_alter_indicatornote_created_by_and_more	2025-05-19 12:13:46.731925+00
36	pmmu	0004_performanceindicator_description	2025-05-19 12:13:46.74491+00
37	sessions	0001_initial	2025-05-19 12:13:46.972944+00
38	statistics	0002_auto_20250407_1453	2025-05-19 12:13:47.514867+00
39	statistics	0003_auto_20250407_1454	2025-05-19 12:13:48.090103+00
40	statistics	0004_auto_20250407_1510	2025-05-19 12:13:48.733266+00
41	statistics	0005_convert_case_categories	2025-05-19 12:13:49.007692+00
42	statistics	0006_create_case_outcomes	2025-05-19 12:13:49.490531+00
43	statistics	0007_create_adjournment_reasons	2025-05-19 12:14:47.499441+00
44	statistics	0008_alter_adjournmentreason_id	2025-05-19 12:14:48.258161+00
45	tasks	0001_initial	2025-05-19 12:14:49.358282+00
46	tasks	0002_auto_20250401_2034	2025-05-19 12:14:49.541515+00
47	tasks	0003_task_start_date	2025-05-19 12:14:49.587444+00
48	organization	0003_department_email	2025-05-19 12:29:41.169877+00
49	tasks	0004_auto_20250521_1337	2025-05-21 13:38:08.787877+00
50	document_management	0002_auto_20250529_1112	2025-05-29 11:13:13.421022+00
51	tasks	0005_auto_20250529_1120	2025-05-29 11:20:17.556004+00
52	tasks	0006_auto_20250529_1127	2025-05-29 11:28:06.233545+00
53	tasks	0007_alter_taskhistory_task_state	2025-05-29 11:28:39.949325+00
54	meetings	0004_auto_20250603_0848	2025-06-03 08:48:19.94051+00
55	meetings	0005_auto_20250603_1421	2025-06-03 14:22:02.969549+00
56	meetings	0006_alter_meeting_unique_together	2025-06-09 12:48:11.050902+00
57	meetings	0002_add_soft_delete	2025-06-10 09:53:48.363322+00
58	meetings	0007_merge_20250610_0953	2025-06-10 09:53:48.376917+00
59	statistics	0009_auto_20250610_1059	2025-06-10 10:59:45.584903+00
60	statistics	0010_unit_dcrt_unique_id	2025-06-10 11:49:33.427169+00
61	statistics	0011_update_unit_ranks	2025-06-10 12:26:21.087177+00
63	statistics	0012_update_unit_ranks	2025-06-10 12:31:28.828704+00
64	statistics	0013_update_unit_ranks	2025-06-10 12:39:46.345024+00
65	statistics	0014_merge_0012_update_unit_ranks_0013_update_unit_ranks	2025-06-10 12:54:10.237184+00
66	statistics	0015_fix_court_ranks	2025-06-10 12:54:10.279118+00
67	statistics	0016_cleanup_tribunal_duplicate	2025-06-10 12:55:18.731883+00
68	tasks	0008_taskhistory_change_description	2025-07-02 09:22:56.206325+00
69	meetings	0008_alter_meeting_unique_together	2025-07-02 10:49:54.704081+00
70	tasks	0009_alter_task_status	2025-07-02 11:27:26.746885+00
71	tasks	0010_auto_20250702_1222	2025-07-02 12:22:55.518529+00
72	memos	0002_auto_20250702_1316	2025-07-02 13:17:10.682311+00
73	meetings	0009_auto_20250702_1316	2025-07-02 13:32:58.75869+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
xctvjrf2wo8t6f9601tkjfmox2uvx6z5	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uH0wX:8gzrOhd4u0yeTiCWaaKlB2M5f7Hgs01nyeUF0PZ-TXQ	2025-06-02 13:54:13.198437+00
fk0l8n59ha5khny9wt8cdqxsc78lksjy	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uHgRY:yR8A3dKg5Z4uglSKzVo0hchM7-6DZMQYd1E9g2MYMfs	2025-06-04 10:13:00.86209+00
71d75h1d9h67qmwbs0xn4e52ys9u57d6	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uJt6C:23AADqljzGwpJFx2gTomwtGPnQ7i1sR-J9ZhrI3bUU4	2025-06-10 12:08:04.243144+00
7spgmcr0al2t0hz89cjqjdrzqk3obqis	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uMMgh:qJTJJEd2MiOo0F-IR_isPouRfFURq_29DGJXt3GDsDA	2025-06-17 08:07:59.297699+00
suwqivcf6lf6mvs61rzla97ia0ko2067	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uMO9A:UxFAPxCU_1XdDUA45XBHIOYe278cJtYF4qZTDKjcK44	2025-06-17 09:41:28.563624+00
f9qwqm79kov5pbwnysulwg9hy31ljq7i	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uMOLs:ebcHF2ZY3znqd7dv6RqMjmYuVrjX0XWKPMKrQPfyOHE	2025-06-17 09:54:36.222185+00
yn8jl117aa4txpdww8aaywcgfhm85bel	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uMOWf:2Zw86bUG3PXlwv5-IjkDZ3dB5c3YHFjpEAdC0y1C0gc	2025-06-17 10:05:45.985856+00
qxokht43a9sao39zssyldf7b1gc1u0v1	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uMOgp:zuQy-oZZ-rUTpTVAskfkQopbWCWBJkmTlSGvn-dRIz4	2025-06-17 10:16:15.600074+00
cfm7l06gyknep0tu3h4v6soemqaulq3p	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uOY9O:5XKJhtw2u24ZdG162omXggnwrcZm-_A3MleQMLqNJzk	2025-06-23 08:46:38.332648+00
nsxxh8mq2kuofznl3t399zg9tjcev49b	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uOu9a:sG1yZ8l7ZTkD4MMQsXNLz9OJ1t6nZZWajKJTn4RfvyA	2025-06-24 08:16:18.845831+00
3q4boxji237svscrddv5vlrxduqqwgen	.eJxVjEEOwiAQRe_C2pChUECX7j0DmYFBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXERgxKn35EwPrnuJD2w3puMrS7zRHJX5EG7vLXEr-vh_h0U7GWrmcGo5DMpsN45Yqe9Po8DZYd6Q9GOgMYkDdZapQEgExIl1IyIisTnC_PeOAc:1uPo6P:3P84G0SaLpZFcK5kL96iCewECy0UiiIEZx4Fcpp8RLA	2025-06-26 20:00:45.025462+00
y21w2zb5yqofapsgakmulhxidhb8zzu3	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uR3XT:gr2Z6tV1SIhRIXngJenuvsFLVybMA__eQNS2ejfr3mg	2025-06-30 06:41:51.01176+00
6f6nvf3pityscovtrxdi2fvmks3h0bmp	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uR6O3:iVo9Dxq-p4KizYzZs1PTTLhqR04xkrwwoP8sEsa1lQ4	2025-06-30 09:44:19.997315+00
cj78ofi4gec8ib33svy6gw297gvf14sj	.eJxVjEEOwiAQRe_C2hBooYBL9z0DmWEGqZqSlHZlvLtt0oVu_3vvv0WEbS1xa7zEicRVaCMuvyNCevJ8EHrAfK8y1XldJpSHIk_a5FiJX7fT_Tso0MpeO3KWkYkVBB8yBkSVUx5MIIsUQtcNQ-IMrHvrXQ_eZq0sMe6m9caJzxc-lzkZ:1uWDAz:lgDuEGzljY6-390JLkkA8EtFqIoRIv6OM7HyePQsasM	2025-07-14 11:59:57.342393+00
dn701fzydp23na0yqlcwyxualp6hncs2	.eJxVjMsOwiAQRf-FtSE8poW6dO83kIFhpGogKe3K-O_apAvd3nPOfYmA21rC1vMSZhJnocXpd4uYHrnugO5Yb02mVtdljnJX5EG7vDbKz8vh_h0U7OVbg0JQyWVPwOTZTUazM-PEFCkZqxWgB88-QRxJWdBxYERWylO2TIN4fwDrRjhh:1uWDNK:1memqsn_h2v8Qev6Ajm9MhI0E7CpECJeeMMh5TZGjy4	2025-07-14 12:12:42.514718+00
g2u03kkfqnntkzhib96idrd8cyrbpnsk	.eJxVjMsOwiAQRf-FtSG8qS7d-w1khgGpGkhKuzL-uyXpQrf3nHPfLMC2lrD1tISZ2IVJdvrdEOIz1QHoAfXeeGx1XWbkQ-EH7fzWKL2uh_t3UKCXUbscMxoD0koEIESypLXwVuSYMmi1C4LOzikVE6KZ7I6SVH7SHkVkny8Zxzio:1uWvKs:_EkPv8D6O_KNEYb_bw6an1J2y9S9j7RlUwLhd0D2Q8s	2025-07-16 11:09:06.550813+00
\.


--
-- Data for Name: document_management_document; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.document_management_document (id, title, description, file, file_type, file_size, tags, storage_type, drive_file_id, drive_view_link, is_confidential, status, password_protected, access_code, object_id, source_module, version, created_at, updated_at, last_accessed, expiry_date, category_id, content_type_id, parent_document_id, uploaded_by_id) FROM stdin;
1	Document for Note: a. Review 2023-2024 ...	Dummy document attached to indicator note for Institutionalize Performance Management	documents/2025/05/19/note_doc_1_1.txt	text/plain	83		local	\N	\N	f	draft	f	\N	1	pmmu	1.0	2025-05-19 12:20:38.847863+00	2025-05-19 12:20:38.847887+00	\N	\N	\N	52	\N	1
2	Document for Note: c. Coordinate PMMUs ...	Dummy document attached to indicator note for Institutionalize Performance Management	documents/2025/05/19/note_doc_1_3.txt	text/plain	97		local	\N	\N	f	draft	f	\N	3	pmmu	1.0	2025-05-19 12:20:38.886672+00	2025-05-19 12:20:38.88672+00	\N	\N	\N	52	\N	1
3	Document for Note: a. Chief Justice...	Dummy document attached to indicator note for Institutionalize Performance Management	documents/2025/05/19/note_doc_1_8.txt	text/plain	68		local	\N	\N	f	draft	f	\N	8	pmmu	1.0	2025-05-19 12:20:39.137447+00	2025-05-19 12:20:39.137467+00	\N	\N	\N	52	\N	1
4	Document for Note: c. Chief Registrar o...	Dummy document attached to indicator note for Institutionalize Performance Management	documents/2025/05/19/note_doc_1_10.txt	text/plain	53		local	\N	\N	f	draft	f	\N	10	pmmu	1.0	2025-05-19 12:20:39.698857+00	2025-05-19 12:20:39.698878+00	\N	\N	\N	52	\N	1
5	Document for Note: d. Judiciary Managem...	Dummy document attached to indicator note for Institutionalize Performance Management	documents/2025/05/19/note_doc_1_11.txt	text/plain	88		local	\N	\N	f	draft	f	\N	11	pmmu	1.0	2025-05-19 12:20:40.33835+00	2025-05-19 12:20:40.33837+00	\N	\N	\N	52	\N	1
6	Document for Note: c. 2nd Quarter Casel...	Dummy document attached to indicator note for Timely preparation and dissemination of caseload statistics	documents/2025/05/19/note_doc_3_19.txt	text/plain	93		local	\N	\N	f	draft	f	\N	19	pmmu	1.0	2025-05-19 12:20:42.067785+00	2025-05-19 12:20:42.067855+00	\N	\N	\N	52	\N	1
7	Document for Note: a. Prepare input on ...	Dummy document attached to indicator note for Facilitate use of Statistics to inform policy	documents/2025/05/19/note_doc_4_21.txt	text/plain	97		local	\N	\N	f	draft	f	\N	21	pmmu	1.0	2025-05-19 12:20:42.253359+00	2025-05-19 12:20:42.253379+00	\N	\N	\N	52	\N	1
8	Document for Note: b. Prepare and submi...	Dummy document attached to indicator note for Facilitate use of Statistics to inform policy	documents/2025/05/19/note_doc_4_22.txt	text/plain	82		local	\N	\N	f	draft	f	\N	22	pmmu	1.0	2025-05-19 12:20:42.43642+00	2025-05-19 12:20:42.436438+00	\N	\N	\N	52	\N	1
9	Document for Note: a. Facilitate establ...	Dummy document attached to indicator note for Institutionalize Quality Management Systems	documents/2025/05/19/note_doc_5_23.txt	text/plain	98		local	\N	\N	f	draft	f	\N	23	pmmu	1.0	2025-05-19 12:20:42.677998+00	2025-05-19 12:20:42.678014+00	\N	\N	\N	52	\N	1
10	Document for Note: c. Coordinate Develo...	Dummy document attached to indicator note for Institutionalize Quality Management Systems	documents/2025/05/19/note_doc_5_25.txt	text/plain	66		local	\N	\N	f	draft	f	\N	25	pmmu	1.0	2025-05-19 12:20:42.927991+00	2025-05-19 12:20:42.928006+00	\N	\N	\N	52	\N	1
11	Document for Note: b. Analyse field rep...	Dummy document attached to indicator note for Enhance Feedback Mechanism	documents/2025/05/19/note_doc_8_37.txt	text/plain	69		local	\N	\N	f	draft	f	\N	37	pmmu	1.0	2025-05-19 12:20:43.661886+00	2025-05-19 12:20:43.661901+00	\N	\N	\N	52	\N	1
12	Document for Note: The Directorate will...	Dummy document attached to indicator note for Implement or follow-up on the implementation of the recommendations from the customer satisfaction survey	documents/2025/05/19/note_doc_12_41.txt	text/plain	46		local	\N	\N	f	draft	f	\N	41	pmmu	1.0	2025-05-19 12:20:44.073865+00	2025-05-19 12:20:44.073881+00	\N	\N	\N	52	\N	1
13	Document for Note: a. Identify training...	Dummy document attached to indicator note for Competency development	documents/2025/05/19/note_doc_14_44.txt	text/plain	99		local	\N	\N	f	draft	f	\N	44	pmmu	1.0	2025-05-19 12:20:44.514762+00	2025-05-19 12:20:44.514777+00	\N	\N	\N	52	\N	1
14	Document for Note: a. Hold quarterly st...	Dummy document attached to indicator note for Enhance Employee Satisfaction and Work Environment	documents/2025/05/19/note_doc_17_54.txt	text/plain	76		local	\N	\N	f	draft	f	\N	54	pmmu	1.0	2025-05-19 12:20:45.076986+00	2025-05-19 12:20:45.077004+00	\N	\N	\N	52	\N	1
15	Document for Note: b. Conduct Employee ...	Dummy document attached to indicator note for Enhance Employee Satisfaction and Work Environment	documents/2025/05/19/note_doc_17_55.txt	text/plain	78		local	\N	\N	f	draft	f	\N	55	pmmu	1.0	2025-05-19 12:20:45.337285+00	2025-05-19 12:20:45.337305+00	\N	\N	\N	52	\N	1
24	staj-strategy-activity-mapping_final.xls	Attachment for Task: Investor Directives Manager		application/wps-office.xls	178688		google_drive	1VS8Y1BglLpFaa6EvAhec_rukWWEpEYpm	https://drive.google.com/file/d/1VS8Y1BglLpFaa6EvAhec_rukWWEpEYpm/view?usp=drivesdk	f	draft	f	\N	45	tasks	1.0	2025-05-29 10:25:01.199377+00	2025-05-29 10:25:01.199392+00	\N	\N	\N	57	\N	1
25	maths  P2 Form 3 End Term 3 2023 Exams .json	Attachment for Task: Investor Directives Manager		application/json	19758		google_drive	1KSprQ4WxWHoS9x6tixTuDjOv3pSGxLsO	https://drive.google.com/file/d/1KSprQ4WxWHoS9x6tixTuDjOv3pSGxLsO/view?usp=drivesdk	f	draft	f	\N	45	tasks	1.0	2025-05-29 10:26:44.45198+00	2025-05-29 10:26:44.451996+00	\N	\N	\N	57	\N	1
26	staj-strategy-activity-mapping_final.xls	Attachment for Task: Investor Tactics Agent		application/wps-office.xls	178688		google_drive	1axvtwAgEwCHDs-9i8LlIZrLT0eilcZzY	https://drive.google.com/file/d/1axvtwAgEwCHDs-9i8LlIZrLT0eilcZzY/view?usp=drivesdk	f	draft	f	\N	48	tasks	1.0	2025-05-29 10:50:38.057185+00	2025-05-29 10:50:38.057202+00	\N	\N	\N	57	\N	1
27	OUK_Data_Science.pdf	Attachment for Task: Investor Tactics Agent		application/pdf	1743343		google_drive	1-LWXebroKMKdmTzHrHGHcw_vABM_dGv7	https://drive.google.com/file/d/1-LWXebroKMKdmTzHrHGHcw_vABM_dGv7/view?usp=drivesdk	f	draft	f	\N	48	tasks	1.0	2025-05-29 10:51:23.129114+00	2025-05-29 10:51:23.129133+00	\N	\N	\N	57	\N	1
29	input.pdf		documents/2025/05/29/input_5qFl9Po.pdf	application/pdf	1608668		local	\N	\N	f	draft	f	\N	54		1.0	2025-05-29 10:56:22.73861+00	2025-05-29 10:56:22.738628+00	\N	\N	\N	57	\N	1
30	Magistrate Court-2022-2023-26-01-2024 09 08 12.xlsx	Attachment for Task: Lead Paradigm Director		application/wps-office.xlsx	14499		google_drive	1MdOLfc8ozKebUeam4dEVvm_dg8HAtwgh	https://drive.google.com/file/d/1MdOLfc8ozKebUeam4dEVvm_dg8HAtwgh/view?usp=drivesdk	f	draft	f	\N	55	tasks	1.0	2025-05-29 10:58:08.04539+00	2025-05-29 10:58:08.045406+00	\N	\N	\N	57	\N	1
31	staj-strategy-activity-mapping2.csv	Attachment for Task: Lead Paradigm Director		text/csv	35864		google_drive	1LC_TVH6BAYqlTDbN-FAIZSe0o7vyPpj7	https://drive.google.com/file/d/1LC_TVH6BAYqlTDbN-FAIZSe0o7vyPpj7/view?usp=drivesdk	f	draft	f	\N	55	tasks	1.0	2025-05-29 11:17:30.78063+00	2025-05-29 11:17:30.780646+00	\N	\N	\N	57	\N	1
32	staj-strategy-activity-mapping.xlsx	Attachment for Task: Corporate Mobility Orchestrator		application/wps-office.xlsx	22024		google_drive	1kcRfpz7DdukCdb60uhQ-rv1js29BZj07	https://drive.google.com/file/d/1kcRfpz7DdukCdb60uhQ-rv1js29BZj07/view?usp=drivesdk	f	draft	f	\N	56	tasks	1.0	2025-05-29 11:38:25.004555+00	2025-05-29 11:38:25.004571+00	\N	\N	\N	57	\N	1
33	OUK_Data_Science.pdf	Attachment for Task: Ngobiro		application/pdf	1743343		google_drive	1ppDSYbISEPpZgqt0RTo3cKO1Dg7rnrq8	https://drive.google.com/file/d/1ppDSYbISEPpZgqt0RTo3cKO1Dg7rnrq8/view?usp=drivesdk	f	draft	f	\N	57	tasks	1.0	2025-05-29 11:45:44.182209+00	2025-05-29 11:45:44.182225+00	\N	\N	\N	57	\N	1
34	CS P2 Form 3 End Term 3 2023 Exams  .json	Attachment for Meeting: International Data Agent		application/json	11892		google_drive	1XGAXjqGh2rCYg2aOMYNVx43sXwtI2QPa	https://drive.google.com/file/d/1XGAXjqGh2rCYg2aOMYNVx43sXwtI2QPa/view?usp=drivesdk	f	draft	f	\N	124	meetings	1.0	2025-06-03 13:25:39.217548+00	2025-06-03 13:25:39.217563+00	\N	\N	\N	33	\N	21
35	staj-strategy-activity-mapping.xlsx	Attachment for Meeting: Future Optimization Facilitator		application/wps-office.xlsx	22024		google_drive	18mp7hMYqGZufAyGBvpA6uQ_wSCtvW9D9	https://drive.google.com/file/d/18mp7hMYqGZufAyGBvpA6uQ_wSCtvW9D9/view?usp=drivesdk	f	draft	f	\N	119	meetings	1.0	2025-06-03 14:28:24.644519+00	2025-06-03 14:28:24.644535+00	\N	\N	\N	33	\N	21
36	staj-strategy-activity-mapping_final.xls	Attachment for Task: Principal Infrastructure Supervisor		application/wps-office.xls	178688		google_drive	1ZgMoHKd0DbmztMShiASOd2LA9WDSFPtj	https://drive.google.com/file/d/1ZgMoHKd0DbmztMShiASOd2LA9WDSFPtj/view?usp=drivesdk	f	draft	f	\N	58	tasks	1.0	2025-06-03 14:30:55.034726+00	2025-06-03 14:30:55.034742+00	\N	\N	\N	57	\N	21
37	6. Sample PMMU Magistrates Court 2021_2022.docx	Attachment for Meeting: National Tactics Planner		application/wps-office.docx	185554		google_drive	1EaKo6lqw3fBbiosiC8hd4VRCpvSq9BLK	https://drive.google.com/file/d/1EaKo6lqw3fBbiosiC8hd4VRCpvSq9BLK/view?usp=drivesdk	f	draft	f	\N	133	meetings	1.0	2025-06-09 09:00:50.148063+00	2025-06-09 09:00:50.148082+00	\N	\N	\N	33	\N	21
38	PMMU System Indicator Raw Score Calculation.docx	Attachment for Meeting: Product Quality Representative		application/wps-office.docx	12897		google_drive	1C_53IpacgZlCbanJJJyuf-cD0UXy3m9i	https://drive.google.com/file/d/1C_53IpacgZlCbanJJJyuf-cD0UXy3m9i/view?usp=drivesdk	f	draft	f	\N	132	meetings	1.0	2025-06-09 09:02:35.904953+00	2025-06-09 09:02:35.904968+00	\N	\N	\N	33	\N	21
39	Acconts (GOK) Surrender Form.docx	Attachment for Meeting: Legacy Creative Associate		application/wps-office.docx	24877		google_drive	14V6SMtPTpsYN-LeZB0YkV41-JNCI35eS	https://drive.google.com/file/d/14V6SMtPTpsYN-LeZB0YkV41-JNCI35eS/view?usp=drivesdk	f	draft	f	\N	134	meetings	1.0	2025-06-09 09:18:37.260753+00	2025-06-09 09:18:37.260768+00	\N	\N	\N	33	\N	21
40	BUGOMA ELC.pdf	Attachment for Task: Dynamic Response Coordinator		application/pdf	285982		google_drive	1HIE9WOVWlToo7tTJadoypBw-CrstFcTD	https://drive.google.com/file/d/1HIE9WOVWlToo7tTJadoypBw-CrstFcTD/view?usp=drivesdk	f	draft	f	\N	59	tasks	1.0	2025-06-09 09:27:09.191295+00	2025-06-09 09:27:09.191312+00	\N	\N	\N	57	\N	21
41	judgement analysis.xlsx	Attachment for Meeting: Product Research Orchestrator		application/wps-office.xlsx	75738		google_drive	1i_day2UJOwGxvzUURXOfnFFufooyuZwR	https://drive.google.com/file/d/1i_day2UJOwGxvzUURXOfnFFufooyuZwR/view?usp=drivesdk	f	draft	f	\N	177	meetings	1.0	2025-06-10 08:44:36.516716+00	2025-06-10 08:44:36.516732+00	\N	\N	\N	33	\N	1
\.


--
-- Data for Name: document_management_documentaccess; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.document_management_documentaccess (id, permission_type, granted_at, expires_at, is_active, document_id, granted_by_id, user_id) FROM stdin;
1	admin	2025-05-19 12:20:38.860966+00	\N	t	1	1	1
2	admin	2025-05-19 12:20:38.90303+00	\N	t	2	1	1
3	admin	2025-05-19 12:20:39.344585+00	\N	t	3	1	1
4	admin	2025-05-19 12:20:40.028909+00	\N	t	4	1	1
5	admin	2025-05-19 12:20:40.574983+00	\N	t	5	1	1
6	admin	2025-05-19 12:20:42.136283+00	\N	t	6	1	1
7	admin	2025-05-19 12:20:42.360706+00	\N	t	7	1	1
8	admin	2025-05-19 12:20:42.502348+00	\N	t	8	1	1
9	admin	2025-05-19 12:20:42.74394+00	\N	t	9	1	1
10	admin	2025-05-19 12:20:42.985733+00	\N	t	10	1	1
11	admin	2025-05-19 12:20:43.67734+00	\N	t	11	1	1
12	admin	2025-05-19 12:20:44.194269+00	\N	t	12	1	1
13	admin	2025-05-19 12:20:44.577299+00	\N	t	13	1	1
14	admin	2025-05-19 12:20:45.209063+00	\N	t	14	1	1
15	admin	2025-05-19 12:20:45.427438+00	\N	t	15	1	1
\.


--
-- Data for Name: document_management_documentactivity; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.document_management_documentactivity (id, action, action_details, ip_address, user_agent, "timestamp", document_id, user_id) FROM stdin;
1	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:38.853073+00	1	1
2	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:38.894026+00	2	1
3	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:39.236364+00	3	1
4	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:39.893407+00	4	1
5	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:40.476692+00	5	1
6	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:42.108106+00	6	1
7	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:42.353153+00	7	1
8	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:42.460721+00	8	1
9	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:42.702627+00	9	1
10	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:42.955605+00	10	1
11	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:43.669367+00	11	1
12	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:44.181614+00	12	1
13	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:44.543983+00	13	1
14	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:45.172979+00	14	1
15	upload	Document uploaded from indicatornote	\N		2025-05-19 12:20:45.398351+00	15	1
\.


--
-- Data for Name: document_management_documentcategory; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.document_management_documentcategory (id, name, description, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: document_management_documentcomment; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.document_management_documentcomment (id, content, created_at, updated_at, author_id, document_id, parent_comment_id) FROM stdin;
1	ffff	2025-05-29 11:16:54.564065+00	2025-05-29 11:16:54.564079+00	1	30	\N
2	dddd	2025-05-29 11:17:30.790007+00	2025-05-29 11:17:30.790024+00	1	31	\N
3	gggg	2025-05-29 11:21:32.8116+00	2025-05-29 11:21:32.811614+00	1	27	\N
4	gggg	2025-05-29 11:21:37.374288+00	2025-05-29 11:21:37.374303+00	1	27	\N
5	ssss	2025-05-29 11:33:01.407647+00	2025-05-29 11:33:01.407663+00	1	26	\N
\.


--
-- Data for Name: home_module; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.home_module (id, name, description, icon_class, url_name, permission_codename) FROM stdin;
1	Document Management	Create, share and manage electronic documents	fas fa-file-alt	document_management:document_list	access_documents
3	Budget	Manage workplans and budgets	fas fa-money-bill-alt	budget:workplan_summary	access_budget
5	Performance	Performance tracking and reporting	fas fa-tachometer-alt	performance:dashboard	access_performance
6	Memos	Internal memos and communications	fas fa-envelope	memos:department_dashboard	access_memos
7	Projects	Track transformative initiatives	fas fa-project-diagram	projects:dashboard	access_projects
8	Reports	Generate and download reports	fas fa-file-pdf	reports:dashboard	access_reports
9	Mail	Manage physical mail	fas fa-envelope	mail:physical_list	access_mail
10	Surveys	Create and manage surveys	fas fa-poll	surveys:dashboard	access_surveys
11	PMMU Evaluation	PMMU Evaluation and Target Setting	fas fa-chart-line	pmmu_evaluation:dashboard	access_pmmu_evaluation
12	Innovations	Innovations and Best Practices	fas fa-lightbulb	innovations:dashboard	access_innovations
2	Meetings	Schedule and manage meetings	fas fa-calendar-alt	meetings:dashboard	access_meetings
4	Statistics	Access and analyze DCRT data	fas fa-chart-bar	statistics:home	access_statistics
\.


--
-- Data for Name: home_module_departments; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.home_module_departments (id, module_id, department_id) FROM stdin;
1	2	1
2	4	4
\.


--
-- Data for Name: innovations_innovation; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.innovations_innovation (id, station, title, is_replication, source_court, category, situation_before, description, solution, replication_potential, individuals_involved, stakeholders_affected, status, submitted_at, approved_at, approved_by_id, court_id, financial_year_id, submitted_by_id) FROM stdin;
\.


--
-- Data for Name: innovations_innovationattachment; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.innovations_innovationattachment (id, file, uploaded_at, innovation_id, uploaded_by_id) FROM stdin;
\.


--
-- Data for Name: mail_mailactivity; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.mail_mailactivity (id, action, notes, "timestamp", location, mail_id, user_id) FROM stdin;
\.


--
-- Data for Name: mail_mailassignment; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.mail_mailassignment (id, assigned_at, due_date, completed, completed_at, notes, current_location, acknowledgment_required, acknowledged, acknowledged_at, acknowledged_by, assigned_by_id, assigned_to_id, mail_id) FROM stdin;
\.


--
-- Data for Name: mail_mailattachment; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.mail_mailattachment (id, name, description, attachment_type, quantity, condition, digital_copy_id, mail_id) FROM stdin;
\.


--
-- Data for Name: mail_mailmovement; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.mail_mailmovement (id, from_location, to_location, "timestamp", notes, received_by, received_at, handler_id, mail_id) FROM stdin;
\.


--
-- Data for Name: mail_physicalmail; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.mail_physicalmail (id, tracking_number, mail_type, subject, description, date_received, date_sent, priority, confidential, file_number, delivery_method, weight, postage_cost, courier_name, courier_tracking_number, status, created_at, updated_at, sender_name, sender_address, sender_phone, recipient_name, recipient_address, recipient_phone, requires_response, response_deadline, created_by_id, department_id, response_mail_id) FROM stdin;
\.


--
-- Data for Name: meetings_meeting; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.meetings_meeting (id, title, meeting_type_id, date, start_time, end_time, meeting_mode, physical_location, virtual_meeting_url, virtual_meeting_id, virtual_meeting_password, virtual_platform, agenda, minutes, status, recording_url, has_recording, created_at, updated_at, department_id, organizer_id, is_deleted, deleted_at, content_type_id, object_id) FROM stdin;
107	ffff ffffff	7	2025-04-05	15:23:00	\N	physical	fff		\N	\N	\N	cccc	\N	scheduled	\N	f	2025-06-03 12:24:30.804178+00	2025-06-03 12:24:30.804195+00	1	21	f	\N	\N	\N
109	ffff ffffff	7	2025-04-02	15:24:00	\N	physical	fff		\N	\N	\N	cccc	\N	scheduled	\N	f	2025-06-03 12:24:54.216469+00	2025-06-03 12:24:54.216483+00	1	21	f	\N	\N	\N
143	Senior Implementation Coordinator	6	2025-06-13	11:19:00	13:27:00	physical	Tenetur quia porro maxime placeat. Aspernatur facere laboriosam explicabo maxime placeat. Voluptatem ad eligendi provident labore excepturi assumenda.		\N	\N	\N	Voluptates iste accusamus rem.	\N	scheduled	\N	f	2025-06-09 11:45:09.317722+00	2025-06-09 11:45:09.317736+00	1	21	f	\N	\N	\N
177	Product Research Orchestrator	7	2025-06-20	05:46:00	06:01:00	physical	Tenetur eos harum nihil adipisci. Optio nisi corrupti tempora laborum. Laborum ipsum ducimus odit pariatur.		\N	\N	\N	Sunt similique vel architecto incidunt ratione veniam sed temporibus.	\N	scheduled	\N	f	2025-06-10 08:39:37.674566+00	2025-06-10 08:39:37.674583+00	1	1	f	\N	\N	\N
111	ffff ffffff	7	2025-04-03	15:26:00	\N	physical	fff		\N	\N	\N	cccc	\N	scheduled	\N	f	2025-06-03 12:26:34.526036+00	2025-06-03 12:26:34.526051+00	1	21	f	\N	\N	\N
145	National Tactics Technician	5	2025-06-30	11:08:00	15:30:00	physical	Neque quam nam aliquam neque odio. Rem quasi vero. Quisquam numquam dignissimos nam ullam officia.		\N	\N	\N	Perspiciatis nisi accusantium tempore qui.	\N	scheduled	\N	f	2025-06-09 11:46:23.10577+00	2025-06-09 11:46:23.105785+00	1	21	f	\N	\N	\N
179	Internal Assurance Orchestrator	5	2025-06-23	10:22:00	14:00:00	physical	Numquam quaerat nesciunt possimus. Totam earum eaque earum odit quis assumenda omnis illo. Fugit nemo atque nulla quas.		\N	\N	\N	Tenetur praesentium assumenda vero accusamus quia ipsum ea non veniam.	\N	scheduled	\N	f	2025-06-10 09:34:30.064495+00	2025-06-10 09:34:30.064512+00	1	1	f	\N	\N	\N
113	Future Applications Supervisor	6	2025-04-24	04:56:00	12:30:00	physical	Vel quisquam autem. Non assumenda porro repellendus doloribus quisquam. Labore hic rem eum consequatur similique quod eos.		\N	\N	\N	Natus ea quisquam ea aut aspernatur nemo aut.	\N	scheduled	\N	f	2025-06-03 12:29:18.352687+00	2025-06-03 12:29:18.352703+00	1	21	f	\N	\N	\N
119	Future Optimization Facilitator	5	2025-06-03	10:57:00	11:51:00	physical	fffff		\N	\N	\N	Nostrum quos incidunt beatae repellat ipsum porro in.	\N	cancelled	\N	f	2025-06-03 13:17:30.666064+00	2025-06-03 14:28:33.961961+00	1	21	f	\N	\N	\N
125	Human Identity Planner	7	2025-06-03	07:13:00	09:12:00	physical	Corporis autem maiores. Aut dolore enim inventore nam eveniet iure natus. Aspernatur sit libero placeat id porro hic impedit quibusdam.		\N	\N	\N	Asperiores unde similique.	\N	scheduled	\N	f	2025-06-03 14:29:52.170552+00	2025-06-03 14:29:52.170567+00	1	21	f	\N	\N	\N
127	Human Assurance Associate	6	2025-06-10	10:16:00	18:16:00	physical	ggggggggggg					Illo aliquid magni harum sit.	\N	scheduled	\N	f	2025-06-09 08:53:36.168074+00	2025-06-09 08:53:36.168089+00	1	21	f	\N	\N	\N
147	Product Division Developer	4	2025-06-09	09:28:00	13:42:00	physical	Dolorum provident necessitatibus quod veniam explicabo qui. Natus nam odio architecto autem cupiditate officiis repellat. Voluptas cupiditate culpa soluta porro ipsam quasi neque ea.		\N	\N	\N	Saepe perferendis rem neque illo saepe molestiae blanditiis ex.	\N	cancelled	\N	f	2025-06-09 12:43:46.635717+00	2025-06-09 12:49:22.54363+00	1	21	f	\N	\N	\N
181	Human Mobility Orchestrator	8	2025-06-02	00:09:00	15:17:00	physical	Eaque cum deleniti consectetur quisquam aliquam ipsum. Veritatis perferendis odit dolor suscipit voluptate. Inventore accusantium commodi explicabo commodi assumenda.		\N	\N	\N	Iure dicta ratione similique molestiae.	\N	scheduled	\N	f	2025-06-10 09:56:57.205147+00	2025-06-10 09:56:57.205161+00	1	1	f	\N	\N	\N
120	Regional Assurance Strategist	5	2025-06-03	06:50:00	07:58:00	physical	Inventore ex adipisci animi autem ut quam praesentium est. Quaerat aliquam ratione. Tempora maxime omnis laborum.		\N	\N	\N	Amet itaque provident odit quis perferendis labore id.	\N	scheduled	\N	f	2025-06-03 13:18:46.969724+00	2025-06-03 13:18:46.969739+00	1	21	f	\N	\N	\N
121	Regional Metrics Assistant	4	2025-06-03	10:31:00	12:27:00	physical	Fuga ex vitae. Labore tempora molestias autem magnam porro debitis. Ex aperiam nulla at.		\N	\N	\N	Excepturi rerum voluptatibus nihil deleniti dolorum ratione fugiat.	\N	scheduled	\N	f	2025-06-03 13:19:19.990818+00	2025-06-03 13:19:19.990833+00	1	21	f	\N	\N	\N
149	District Paradigm Agent	4	2025-06-04	02:48:00	19:34:00	physical	Aperiam non quod iusto accusantium perferendis sit necessitatibus. Fugiat saepe velit itaque qui minus placeat exercitationem deleniti delectus. Velit porro veniam.		\N	\N	\N	Doloremque illum quod pariatur accusamus quidem.	\N	scheduled	\N	f	2025-06-09 12:52:11.824859+00	2025-06-09 12:52:11.824874+00	1	21	f	\N	\N	\N
183	Regional Markets Associate	4	2025-06-11	13:50:00	20:59:00	physical	Repellendus excepturi fugit voluptas ipsam delectus quis ipsa omnis aperiam. Eligendi quibusdam consectetur nostrum ipsum rerum debitis. Odio praesentium consequuntur nesciunt nam illum.		\N	\N	\N	Ut libero maxime quasi architecto ex accusamus voluptates.	\N	scheduled	\N	f	2025-06-10 09:57:27.787505+00	2025-06-10 09:57:27.787517+00	1	1	f	\N	\N	\N
122	Product Security Consultant	1	2025-06-03	05:37:00	16:30:00	physical	Nihil itaque voluptates voluptatem laudantium vitae repellat adipisci mollitia temporibus. Necessitatibus deserunt explicabo nostrum praesentium. At suscipit quasi odio.		\N	\N	\N	Totam minima voluptas quos voluptatem adipisci molestias placeat.	\N	in_progress	\N	f	2025-06-03 13:19:47.691178+00	2025-06-03 14:16:47.731317+00	1	21	f	\N	\N	\N
130	Customer Security Liaison	6	2025-07-29	14:54:00	07:24:00	hybrid	\N	\N	\N	\N	\N	Harum fugiat iure temporibus.	\N	scheduled	\N	f	2025-06-09 08:56:05.668399+00	2025-06-09 08:56:05.668416+00	1	21	f	\N	\N	\N
131	Human Division Designer	3	2024-11-27	00:33:00	02:09:00	hybrid	\N	\N	\N	\N	\N	Exercitationem tempora est qui ipsam voluptate.	\N	scheduled	\N	f	2025-06-09 08:58:20.760043+00	2025-06-09 08:58:20.760059+00	1	21	f	\N	\N	\N
123	Lead Branding Officer	7	2025-06-03	07:46:00	08:43:00	physical	Molestiae esse vero. Odit exercitationem labore similique similique impedit sapiente non ad minus. Consectetur nostrum enim odio eius voluptate suscipit nemo.		\N	\N	\N	Repellendus nostrum consequatur.	\N	cancelled	\N	f	2025-06-03 13:20:16.122608+00	2025-06-09 12:51:47.526758+00	1	21	f	\N	\N	\N
151	Legacy Integration Administrator	8	2025-06-09	09:33:00	16:58:00	physical	Omnis repellat praesentium porro animi ipsam. Eum iusto repellendus. Odio facere voluptas.		\N	\N	\N	Quas explicabo repellat.	\N	scheduled	\N	f	2025-06-09 12:52:26.46863+00	2025-06-09 12:52:26.468646+00	1	21	f	\N	\N	\N
185	Direct Implementation Strategist	6	2025-06-13	09:00:00	08:37:00	physical	Repellat non consequuntur enim ipsum enim. Voluptatibus amet ea ea. Rem repudiandae ullam iste excepturi laudantium quis distinctio repellendus quos.		\N	\N	\N	Corrupti in quis laboriosam sunt et.	\N	scheduled	\N	f	2025-06-10 09:57:46.572326+00	2025-06-10 09:57:46.572348+00	1	1	f	\N	\N	\N
124	International Data Agent	2	2025-06-03	12:25:00	17:15:00	physical	Quam voluptate ea. Iusto itaque vel. Magni eaque voluptatum quo ipsum architecto provident facilis ipsum.		\N	\N	\N	Excepturi vel repudiandae modi deleniti placeat cum reprehenderit pariatur dolorum.	\N	scheduled	\N	f	2025-06-03 13:23:03.292087+00	2025-06-03 13:23:03.292103+00	1	21	f	\N	\N	\N
132	Product Quality Representative	7	2025-06-23	11:00:00	17:39:00	physical	\N	\N	\N	\N	\N	Dolor repellat dolor fugiat explicabo similique quidem id pariatur ducimus.	\N	scheduled	\N	f	2025-06-09 08:59:17.125037+00	2025-06-09 08:59:17.12505+00	1	21	f	\N	\N	\N
186	Principal Marketing Agent	4	2025-06-10	06:59:00	18:57:00	physical	Doloribus illo dicta. Doloremque voluptates iste. Quas doloremque est maiores soluta in quod ea illo.		\N	\N	\N	Atque vero inventore nostrum illum quasi ex nobis.	\N	in_progress	\N	f	2025-06-10 09:58:02.318487+00	2025-06-30 11:07:42.304075+00	1	1	f	\N	\N	\N
133	National Tactics Planner	2	2026-01-27	00:39:00	20:03:00	physical	Aperiam quas illum iure vitae nemo quod ipsam illo. Porro aut esse aut. Odio voluptatibus optio.	\N	\N	\N	\N	2024-11-13 11:51:46	\N	scheduled	\N	f	2025-06-09 09:00:20.277132+00	2025-06-09 09:00:20.277146+00	1	21	f	\N	\N	\N
153	Future Assurance Officer	7	2025-06-16	16:26:00	17:29:00	physical	Nulla cumque placeat ducimus ex asperiores maxime. Dolorum amet nulla iste. Sequi dicta voluptatem iste quaerat ducimus sit quis.		\N	\N	\N	Nihil expedita expedita.	\N	scheduled	\N	f	2025-06-09 12:53:09.560901+00	2025-06-09 12:53:09.560915+00	1	21	f	\N	\N	\N
134	Legacy Creative Associate	7	2025-06-09	03:35:00	11:59:00	physical	ddddd	\N	\N	\N	\N	Maiores neque omnis.	\N	completed	\N	f	2025-06-09 09:10:30.108314+00	2025-06-09 11:44:26.229926+00	1	21	f	\N	\N	\N
135	Regional Usability Planner	3	2025-06-11	15:41:00	21:06:00	physical	Eum aliquam sunt officiis impedit quos reprehenderit tenetur alias rerum. Expedita voluptatum deserunt quae atque architecto itaque quibusdam. Hic culpa molestias magnam error soluta a minus earum.		\N	\N	\N	Perspiciatis omnis error repellat nemo.	\N	scheduled	\N	f	2025-06-09 09:12:20.972482+00	2025-06-09 09:12:20.972497+00	1	21	f	\N	\N	\N
169	Corporate Mobility Representative	5	2025-06-04	12:39:00	13:37:00	physical	Fugiat similique tempora necessitatibus accusamus quas aliquam. Voluptates optio harum deserunt iusto consectetur voluptatibus. Beatae fugiat similique sapiente dolor totam fugit saepe omnis.		\N	\N	\N	Voluptatem unde itaque nostrum rerum nulla iusto odit tempore deserunt.	\N	scheduled	\N	f	2025-06-10 08:34:07.517852+00	2025-06-10 08:34:07.517867+00	1	1	f	\N	\N	\N
137	Direct Research Orchestrator	5	2025-06-12	07:16:00	08:29:00	physical	Porro voluptatibus vel eligendi officiis nulla quae suscipit pariatur. Saepe exercitationem explicabo debitis perferendis iure at voluptatum. Suscipit perspiciatis iste consectetur harum excepturi quas.		\N	\N	\N	Tenetur nesciunt soluta molestiae dolorem incidunt culpa.	\N	scheduled	\N	f	2025-06-09 09:12:51.321567+00	2025-06-09 09:12:51.321583+00	1	21	f	\N	\N	\N
171	Direct Response Associate	7	2025-06-30	15:59:00	17:24:00	physical	Ipsam quisquam beatae iusto molestias. Voluptas voluptatibus quaerat amet quas ut necessitatibus enim exercitationem. Cumque magnam vel facere impedit voluptate placeat et deleniti quo.		\N	\N	\N	Ad nulla expedita ea molestias.	\N	cancelled	\N	f	2025-06-10 08:34:52.931923+00	2025-06-10 08:35:00.113879+00	1	1	f	\N	\N	\N
139	Principal Security Assistant	7	2025-06-05	02:26:00	04:33:00	physical	Expedita sapiente dolores corrupti ex quia ad dolor. Iusto est tempora. Velit eum architecto.		\N	\N	\N	Praesentium vel dolore autem.	\N	scheduled	\N	f	2025-06-09 09:35:52.576004+00	2025-06-09 09:35:52.576039+00	1	21	f	\N	\N	\N
173	Chief Infrastructure Consultant	4	2025-06-12	01:01:00	02:58:00	physical	Voluptas nisi fugiat facere officiis accusamus. Praesentium eum tenetur perspiciatis reprehenderit aut. Ab debitis nihil consequuntur fugit distinctio rem.		\N	\N	\N	Provident numquam dolor.	\N	completed	\N	f	2025-06-10 08:36:54.10261+00	2025-06-10 09:54:29.447539+00	1	1	f	\N	\N	\N
141	National Metrics Executive	7	2025-06-06	13:36:00	14:42:00	physical	Optio qui quia perferendis temporibus quas corrupti. Iure facilis magni consequatur hic est doloribus. Unde consequatur rem illum aspernatur reiciendis accusamus earum voluptas ut.		\N	\N	\N	Eius necessitatibus dolor quasi veritatis.	\N	scheduled	\N	f	2025-06-09 09:36:20.69951+00	2025-06-09 09:36:20.699525+00	1	21	f	\N	\N	\N
175	Corporate Marketing Designer	1	2025-06-11	01:30:00	14:16:00	physical	Architecto ipsa incidunt quam animi earum. Magnam accusantium numquam itaque veniam eos repudiandae atque. Vitae illum nesciunt.		\N	\N	\N	Perferendis commodi nostrum minus officia molestiae.	\N	scheduled	\N	f	2025-06-10 08:37:32.028218+00	2025-06-10 09:53:55.547276+00	1	1	t	2025-06-10 09:53:55.547135+00	\N	\N
\.


--
-- Data for Name: meetings_meetingaction; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.meetings_meetingaction (id, description, due_date, assigned_to_id, meeting_id) FROM stdin;
\.


--
-- Data for Name: meetings_meetingdocument; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.meetings_meetingdocument (id, document_type, notes, uploaded_at, updated_at, document_id, meeting_id) FROM stdin;
\.


--
-- Data for Name: meetings_meetingparticipant; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.meetings_meetingparticipant (id, role, meeting_id, participant_id, email, is_external, mobile, name) FROM stdin;
1	attendee	107	21		f		
3	attendee	109	21		f		
41	attendee	143	21		f		
5	attendee	111	21		f		
43	attendee	145	21		f		
7	attendee	113	21		f		
13	attendee	113	2		f		
21	attendee	119	16		f		
25	attendee	127	21		f		
45	attendee	147	21		f		
14	attendee	113	16		f		
22	guest	124	11		f		
15	attendee	119	21		f		
23	attendee	125	21		f		
47	attendee	149	21		f		
16	attendee	120	21		f		
28	attendee	130	21		f		
48	attendee	151	21		f		
17	attendee	121	21		f		
29	attendee	131	21		f		
49	attendee	153	21		f		
18	attendee	122	21		f		
30	attendee	132	21		f		
50	attendee	169	1		f		
19	attendee	123	21		f		
31	attendee	133	21		f		
51	attendee	171	1		f		
20	attendee	124	21		f		
32	attendee	134	21		f		
52	attendee	173	1		f		
33	attendee	135	21		f		
53	attendee	175	1		f		
54	attendee	177	1		f		
35	attendee	137	21		f		
55	attendee	179	1		f		
56	attendee	181	1		f		
37	attendee	139	21		f		
57	attendee	183	1		f		
58	attendee	185	1		f		
39	attendee	141	21		f		
59	attendee	186	1		f		
\.


--
-- Data for Name: meetings_meetingtype; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.meetings_meetingtype (id, name, description, is_active, created_at, updated_at) FROM stdin;
1	Department Internal	Internal meetings within a department	t	2025-05-19 12:13:42.083249+00	2025-05-19 12:13:42.083275+00
2	With Director	Meetings with department director	t	2025-05-19 12:13:42.084957+00	2025-05-19 12:13:42.084978+00
3	Committee Meeting	Committee or board meetings	t	2025-05-19 12:13:42.085784+00	2025-05-19 12:13:42.085802+00
4	Training Session	Training or workshop sessions	t	2025-05-19 12:13:42.086435+00	2025-05-19 12:13:42.086452+00
5	Project Review	Project progress review meetings	t	2025-05-19 12:13:42.087154+00	2025-05-19 12:13:42.087169+00
6	Stakeholder Meeting	Meetings with external stakeholders	t	2025-05-19 12:13:42.08765+00	2025-05-19 12:13:42.087664+00
7	Strategy Session	Strategic planning meetings	t	2025-05-19 12:13:42.088195+00	2025-05-19 12:13:42.08821+00
8	Other	Other types of meetings	t	2025-05-19 12:13:42.088875+00	2025-05-19 12:13:42.088893+00
\.


--
-- Data for Name: memos_memo; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memo (id, title, reference_number, memo_type, content, status, created_at, updated_at, published_at, version_number, is_confidential, external_recipient, external_organization, tags, file_number, created_by_id, department_id, document_id, template_id, content_type_id, object_id) FROM stdin;
\.


--
-- Data for Name: memos_memo_recipient_departments; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memo_recipient_departments (id, memo_id, department_id) FROM stdin;
\.


--
-- Data for Name: memos_memo_recipient_users; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memo_recipient_users (id, memo_id, customuser_id) FROM stdin;
\.


--
-- Data for Name: memos_memoactivity; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memoactivity (id, action, action_details, "timestamp", ip_address, user_agent, document_id, memo_id, user_id) FROM stdin;
\.


--
-- Data for Name: memos_memoapproval; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memoapproval (id, status, comments, approved_at, level, approver_id, memo_id, signature_document_id) FROM stdin;
\.


--
-- Data for Name: memos_memocomment; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memocomment (id, content, created_at, updated_at, is_internal, memo_id, parent_id, user_id) FROM stdin;
\.


--
-- Data for Name: memos_memocomment_attachments; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memocomment_attachments (id, memocomment_id, document_id) FROM stdin;
\.


--
-- Data for Name: memos_memotemplate; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memotemplate (id, name, description, content, memo_type, created_at, updated_at, is_active, created_by_id, department_id) FROM stdin;
\.


--
-- Data for Name: memos_memoversion; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.memos_memoversion (id, version_number, content, created_at, comments, created_by_id, document_id, memo_id) FROM stdin;
\.


--
-- Data for Name: organization_department; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.organization_department (id, name, description, created_at, is_active, email) FROM stdin;
1	Director's Office	Office of the Director	2025-05-19 12:18:50.929566+00	t	directors.office@judiciary.go.ke
2	Strategic planning and implementation Department		2025-05-19 12:18:50.950055+00	t	strategic.planning@judiciary.go.ke
3	Performance monitoring and evaluation Department		2025-05-19 12:18:50.957665+00	t	monitoring.evaluation@judiciary.go.ke
4	Research and data analytics Department		2025-05-19 12:18:50.965945+00	t	research.analytics@judiciary.go.ke
5	Quality assurance and innovation Department		2025-05-19 12:18:50.974264+00	t	quality.assurance@judiciary.go.ke
\.


--
-- Data for Name: organization_role; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.organization_role (id, title, job_group, description, is_active, created_at, department_id) FROM stdin;
2	Assistant Director		Assistant Director role in the organization	t	2025-05-21 11:57:57.058322+00	1
3	Programme Officer		Programme Officer role in the organization	t	2025-05-21 11:57:57.097238+00	1
4	Office Assistant		Office Assistant role in the organization	t	2025-05-21 11:57:57.106283+00	1
5	Director	JSG5		t	2025-06-03 12:24:18.097474+00	1
\.


--
-- Data for Name: organization_role_permissions; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.organization_role_permissions (id, role_id, permission_id) FROM stdin;
\.


--
-- Data for Name: organization_userrole; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.organization_userrole (id, assigned_at, is_active, role_id, user_id) FROM stdin;
1	2025-05-21 12:04:24.419908+00	t	2	2
2	2025-05-21 12:04:51.6348+00	t	2	3
3	2025-05-21 12:04:51.981795+00	t	2	4
4	2025-05-21 12:04:52.268033+00	t	3	5
5	2025-05-21 12:04:52.525802+00	t	3	6
6	2025-05-21 12:04:52.800634+00	t	3	7
7	2025-05-21 12:04:53.092392+00	t	3	8
8	2025-05-21 12:04:53.350642+00	t	3	9
9	2025-05-21 12:04:53.664186+00	t	3	10
10	2025-05-21 12:04:53.909645+00	t	3	11
11	2025-05-21 12:04:54.240645+00	t	3	12
12	2025-05-21 12:04:54.492496+00	t	3	13
13	2025-05-21 12:04:54.892187+00	t	3	14
14	2025-05-21 12:04:55.159048+00	t	3	15
15	2025-05-21 12:04:55.505474+00	t	3	16
16	2025-05-21 12:04:55.758955+00	t	3	17
17	2025-05-21 12:04:56.093412+00	t	4	18
18	2025-05-21 12:04:56.342377+00	t	4	19
19	2025-05-21 12:04:56.633839+00	t	4	20
20	2025-06-03 12:24:18.151569+00	t	5	21
\.


--
-- Data for Name: pmmu_financialyearperformance; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.pmmu_financialyearperformance (id, target, baseline, actual, financial_year_id, indicator_id) FROM stdin;
\.


--
-- Data for Name: pmmu_indicatorcategory; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.pmmu_indicatorcategory (id, name, display_name, description) FROM stdin;
\.


--
-- Data for Name: pmmu_indicatornote; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.pmmu_indicatornote (id, note_text, created_at, created_by_id, indicator_id) FROM stdin;
1	a. Review 2023-2024 performance management guidelines	2025-05-19 12:20:38.835739+00	1	1
2	b. Coordinate PMMU evaluations and target setting to all courts and units within the first half of the financial year	2025-05-19 12:20:38.869136+00	1	1
3	c. Coordinate PMMUs evaluation for all Implementing Units	2025-05-19 12:20:38.877671+00	1	1
4	d. Evaluate compliance of Service Delivery Standards and prepare annual report	2025-05-19 12:20:38.910752+00	1	1
5	e. Conduct annual Performance Management and Measurement sensitisation for Heads of Stations and Deputy Registrars	2025-05-19 12:20:38.921809+00	1	1
6	f. Facilitate annual AJPMC engagement on status and feedback of PMMU implementation to improve the process.	2025-05-19 12:20:38.969448+00	1	1
7	g. Undertake PMMU briefs for the following;	2025-05-19 12:20:38.994149+00	1	1
8	a. Chief Justice	2025-05-19 12:20:39.05218+00	1	1
9	b. Deputy Chief Justice	2025-05-19 12:20:39.423959+00	1	1
10	c. Chief Registrar of the Judiciary	2025-05-19 12:20:39.535634+00	1	1
11	d. Judiciary Management Team	2025-05-19 12:20:40.226723+00	1	1
12	h. Identify and recommend new/reviewed performance measurement indicators and submit to AJPMC for adoption	2025-05-19 12:20:40.602537+00	1	1
13	a. Sensitize staff in at least 200 courts on data management.	2025-05-19 12:20:40.712284+00	1	2
14	b. Facilitate case audits in 10 courts	2025-05-19 12:20:40.885719+00	1	2
15	c. Improve caseload data accuracy across the Judiciary by 3 percent.	2025-05-19 12:20:41.126353+00	1	2
16	d. Update the data dictionary in liaison with the registrars as need arises.	2025-05-19 12:20:41.429935+00	1	2
17	a. Annual Caseload Statistics Report for FY 2023/24 by 5th August 2024.	2025-05-19 12:20:41.820287+00	1	3
18	b. 1st Quarter Caseload Report 2024/25 by 5th November 2024.	2025-05-19 12:20:41.853318+00	1	3
19	c. 2nd Quarter Caseload Report 2024/25 by 5th February 2025.	2025-05-19 12:20:41.95059+00	1	3
20	d. 3rd Quarter Caseload Report 2024/25 by 5th May 2025.	2025-05-19 12:20:42.144014+00	1	3
21	a. Prepare input on caseload statistics for the SOJAR Report 2023/24.	2025-05-19 12:20:42.226596+00	1	4
22	b. Prepare and submit draft performance reports of individual Judges and Judicial officers for JSC within the timelines specified as per request.	2025-05-19 12:20:42.423062+00	1	4
23	a. Facilitate establishment of the Judiciary ISO-QMS Steering Committee	2025-05-19 12:20:42.636033+00	1	5
24	b. Develop a Judiciary ISO-QMS Road Map	2025-05-19 12:20:42.864642+00	1	5
25	c. Coordinate Development of ISO-QMS Procedures for NCAJ	2025-05-19 12:20:42.889023+00	1	5
26	a. Collate and review and publish Service Delivery Innovations	2025-05-19 12:20:43.127344+00	1	6
27	b. Review and Disseminate Service Delivery Innovations for Replications	2025-05-19 12:20:43.170231+00	1	6
28	c. Develop and Maintain a Service Delivery Innovations Online-Repository	2025-05-19 12:20:43.194032+00	1	6
29	d. Undertake and disseminate 1 research on topical issue to inform policy	2025-05-19 12:20:43.236634+00	1	6
30	a. Prepare and disseminate quarterly statistical reports within 30 days from the close of submission by courts	2025-05-19 12:20:43.352407+00	1	7
31	b. Prepare and disseminate quarterly M&E reports within 5 days from receipt of statistical report	2025-05-19 12:20:43.410797+00	1	7
32	c. Prepare ad-hoc reports within 7 days after receipt of the request	2025-05-19 12:20:43.436356+00	1	7
33	d. Prepare 2023-2024 PMMUs evaluation report by 30th June 2025	2025-05-19 12:20:43.478827+00	1	7
34	e. Evaluate the Judiciary Strategic Plan 2019-2023	2025-05-19 12:20:43.576374+00	1	7
35	f. Track implementation of multi-door approach to justice programs such as AJS, CAM, and address emerging issues and report to management	2025-05-19 12:20:43.619841+00	1	7
36	a. Analyse Judiciary dialogue feedback and disseminate the findings	2025-05-19 12:20:43.644066+00	1	8
37	b. Analyse field report from PMMU evaluation exercise and disseminate the findings to AJPMC and management	2025-05-19 12:20:43.652456+00	1	8
38	a. Ensure 100% absorption of the budget as per the approved work plan	2025-05-19 12:20:43.744086+00	1	9
39	b. Implement energy saving initiatives	2025-05-19 12:20:43.885+00	1	10
40	The Directorate will track compliance of all the Service Delivery Charter standards	2025-05-19 12:20:43.952392+00	1	11
41	The Directorate will conduct one survey that involves court users and disseminate the findings	2025-05-19 12:20:44.027283+00	1	12
42	a. Replicate/adopt any relevant innovations OR	2025-05-19 12:20:44.26111+00	1	13
43	b. May come up with one service delivery innovation	2025-05-19 12:20:44.307318+00	1	13
44	a. Identify training gaps and facilitate relevant training	2025-05-19 12:20:44.474193+00	1	14
45	a. Continue sensitizing members of staff on dangers of corruption in staff meetings	2025-05-19 12:20:44.627323+00	1	15
46	b. Document and maintain records of all reported corruption related issues from various sources including the following;	2025-05-19 12:20:44.702182+00	1	15
47	Complaints/corruption feedback	2025-05-19 12:20:44.760673+00	1	15
48	Oversight bodies	2025-05-19 12:20:44.769331+00	1	15
49	C. Implement the recommendations of corruption prevalence surveys and system audits by DSPOP, EACC, and other public oversight bodies.	2025-05-19 12:20:44.777416+00	1	15
50	d. Implement corruption prevention action plans by integrity officers and submit quarterly reports to OJO and OCRJ.	2025-05-19 12:20:44.836761+00	1	15
51	e. Implement strategies to address reported and other corruption eradication activities.	2025-05-19 12:20:44.869863+00	1	15
52	a. Implement staff welfare programme¹	2025-05-19 12:20:45.019275+00	1	16
53	b. Organize one team building event for staff²	2025-05-19 12:20:45.027354+00	1	16
54	a. Hold quarterly staff meetings, emerging issues affecting staff welfare and report progress in the subsequent meetings.	2025-05-19 12:20:45.044102+00	1	17
55	b. Conduct Employee Satisfaction and Work Environment Survey³ and disseminate the findings	2025-05-19 12:20:45.235818+00	1	17
\.


--
-- Data for Name: pmmu_performanceindicator; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.pmmu_performanceindicator (id, name, unit_of_measure, weight, subcategory_id, description) FROM stdin;
1	Institutionalize Performance Management	%	10	\N	
2	Enhance Data Governance	%	10	\N	
3	Timely preparation and dissemination of caseload statistics	%	10	\N	
4	Facilitate use of Statistics to inform policy	%	5	\N	
5	Institutionalize Quality Management Systems	%	8	\N	
6	Promote Service Delivery Innovations	%	7	\N	
7	Enhance Reporting on Programs and Projects	%	10	\N	
8	Enhance Feedback Mechanism	%	10	\N	
9	Compliance with the budget	%	3	\N	
10	Greening Initiatives	%	2	\N	
11	Compliance with Service Delivery Charter Standards	%	5	\N	
12	Implement or follow-up on the implementation of the recommendations from the customer satisfaction survey	%	5	\N	
13	Service improvement Innovations	No.	4	\N	
14	Competency development	%	6	\N	
15	Corruption Prevention & Eradication	%	2	\N	
16	Improve Employee wellness	%	1	\N	
17	Enhance Employee Satisfaction and Work Environment	%	2	\N	
\.


--
-- Data for Name: pmmu_pmmu; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.pmmu_pmmu (id, name, description, created_at, updated_at, financial_year_id) FROM stdin;
1	Performance Management & Measurement Understanding 2024-2025	This PMMU Understanding outlines the agreement between The Chief Registrar of the Judiciary and The Director, Strategy Planning and Organizational Productivity.	2025-05-19 12:20:03.810447+00	2025-05-19 12:20:03.810462+00	1
2	Performance Management & Measurement Understanding 2024-2025	This PMMU Understanding outlines the agreement between The Chief Registrar of the Judiciary and The Director, Strategy Planning and Organizational Productivity.	2025-05-19 12:20:38.812722+00	2025-05-19 12:20:38.812748+00	1
\.


--
-- Data for Name: statistics_adjournmentreason; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_adjournmentreason (id, name, description, unit_rank_id) FROM stdin;
1	Advocate not present	\N	4
2	Advocate not ready	\N	4
3	Court on its own motion	\N	4
4	Death of a party	\N	4
5	Expert report not ready	\N	4
6	File missing	\N	4
7	Judgment not ready	\N	4
8	Judicial officer on transfer	\N	4
9	Matter not cause listed	\N	4
10	No proof of service	\N	4
11	No reason recorded	\N	4
12	Partie(s) not present	\N	4
13	Partie(s) not ready	\N	4
14	Parties to Negotiate	\N	4
15	Ruling not ready	\N	4
16	Submissions not ready	\N	4
17	Typed proceedings not ready	\N	4
18	Witness not present	\N	4
19	Witness not ready	\N	4
20	Court Indisposed	\N	4
21	Public Holiday	\N	4
\.


--
-- Data for Name: statistics_caseactivitytype; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_caseactivitytype (id, name, description, unit_rank_id) FROM stdin;
\.


--
-- Data for Name: statistics_casecategory; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_casecategory (id, name, code, description, unit_rank_id) FROM stdin;
1	Appeals	ELRCA	ELRC Appeals cases	1
2	Claim/Causes	ELRCC	ELRC Claim/Causes cases	1
3	Collective Bargaining Agreements (CBAs)	ELRCBA	ELRC Collective Bargaining Agreements (CBAs) cases	1
4	Judicial Review	ELRCJR	ELRC Judicial Review cases	1
5	Miscellaneous Applications	ELRCMISC	ELRC Miscellaneous Applications cases	1
6	Petitions	ELRCPET	ELRC Petitions cases	1
\.


--
-- Data for Name: statistics_caseoutcome; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_caseoutcome (id, name, description, unit_rank_id) FROM stdin;
\.


--
-- Data for Name: statistics_dcrtdata; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_dcrtdata (id, today_date_day, today_date_month, today_date_year, name_of_court, case_number_number, case_number_day, case_number_month, case_number_year, appeal_number_court_name, appeal_number_code, appeal_number_number, appeal_number_year, specific_case_type, judicial_officer_1, judicial_officer_2, judicial_officer_3, judicial_officer_4, judicial_officer_5, judicial_officer_6, judicial_officer_7, judicial_officer_8, case_coming_for, case_outcome, adjournment_reason, date_of_next_activity_day, date_of_next_activity_month, date_of_next_activity_year, no_of_plaintiffs_or_appellants_male, no_of_plaintiffs_or_appellants_female, no_of_plaintiffs_or_appellants_organization, no_of_defendants_accused_male, no_of_defendants_accused_female, no_of_defendants_accused_organization, parties_have_legal_representation, no_of_witnesses_in_court_d, no_of_witnesses_in_court_w, no_of_accused_remanded, last_date_of_submission_of_case_file_day, last_date_of_submission_of_case_file_month, last_date_of_submission_of_case_file_year, remarks, division_id, financial_quarter_id, financial_year_id, month_id, unit_id, case_number_code_id) FROM stdin;
\.


--
-- Data for Name: statistics_division; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_division (id, name, is_active, code, deleted_at) FROM stdin;
1	Supreme Court Petition	f	SPC	\N
2	Supreme Court Advisory Opinion/Reference	t	SCAOR	\N
3	Supreme Court 	t	SC	\N
4	Supreme Court Petition Application	f	NULL	\N
5	Civil Division	t	CC	\N
6	Criminal  Division	f	CRA	\N
7	High Court Criminal	t	Criminal	\N
8	High Court Commercial and Tax	t	 Commercial 	\N
9	High Court Civil	f	HCC	\N
10	High Court Family	t	Family	\N
11	High Court Judicial Review	f	HCJR	\N
12	High Court Constitution and Human Rights	f	CHR	\N
13	Magistrate Court Civil Case 	f	NULL	\N
14	Magistrate Court Civil Case Miscellaneous 	f	NULL	\N
15	Magistrate Court Criminal	t	MC - Criminal	\N
16	Magistrate Court Criminal Case Miscellaneous 	f	NULL	\N
17	Magistrate Court Traffic Case 	f	NULL	\N
18	Magistrate Court Election Petitions 	f	NULL	\N
19	Magistrate Court Succession Matter 	f	NULL	\N
20	Magistrate Court Children	f	Children	\N
21	Kadhi Court	t	KC	\N
22	Magistrate Court Anti Corruption	t	MCAC	\N
23	High Court Anti Corruption and Economic Crimes	f	ACEC	\N
24	Environment and Land Court	t	ELC	\N
25	Environment and Land Appeal	f	NULL	\N
26	Environment and Land Judiciary Review	f	NULL	\N
27	Environment and Land Miscellaneous	f	NULL	\N
28	Environment and Land Petitions	f	NULL	\N
29	Employment and Labour Relations Court	t	ELRC	\N
30	Employment and Labour Relations Judicial Review	f	NULL	\N
31	Employment and Labour Relations CBA	f	NULL	\N
32	Employment and Labour Relations Petitions	f	NULL	\N
33	Employment and Labour Relations Miscellaneous	f	NULL	\N
34	Employment and Labour Relations Appeal	f	NULL	\N
35	Supreme Court Presidential Election Petition	f	NULL	\N
36	Magistrate Court Commercial	t	MCC	\N
37	Accused Division	f	NULL	\N
38	Environment & Land Matters (OS)	f	NULL	\N
39	xxxxxx1111111111111	f	xxxx11	\N
40	XXXXXXXXX	f	x	\N
41	High Court Criminal - deleted	f	CRM	\N
42	Magistrate Court Traffic	f	MCTR	\N
43	Magistrate Court Criminal	t	MCCR	\N
44	CHR and JR	t	CHR.JR	\N
45	Magistrate Court Civil	f	MCCD	\N
46	High Court Div	f	HC.DIV	\N
47	Magistrate Court	t	MCD	\N
48	Magistrate Court Family	t	MC - Family	\N
49	Nairobi	t	NRB	\N
50	Nairobi	t	NRB	\N
51	Court Annexed Mediation	t	CAM	\N
52	The National Environment Tribunal	t	NET	\N
53	Meru Environment and Land Court	t	MERUELC	\N
54	MERU HIGH COURT	t	MERUHC	\N
55	Meru Magistrate Court	t	MERUMC	\N
56	Sports Disputes Tribunal	t	SDT	\N
57	Court of Appeal	t	COA	\N
58	Tribunal	t	TR	\N
59	Transport Licensing Appeals Board	t	TLAB	\N
60	Advocates Disciplinary Tribunal	t	ADT	\N
61	Auctioneers Licensing Board	t	ALB	\N
62	Nairobi	t	NBI	\N
63	Communications and Multimedia Appeals Tribunal 	f	CAMAT	\N
64	Legal Education Appeals Tribunal 	f	LEAT	\N
65	Micro and Small Enterprise Tribunal 	t	MASET	\N
66	Competent Authority Tribunal 	f	CAT	\N
67	Kenya Institute of Supplies Management Elections Committee	t	KISM	\N
68	Education Appeals Tribunal	t	EAT	\N
69	HIV Tribunal	t	HAT	\N
70	Kajiado	t	KJD	\N
71	Mombasa	t	MSA	\N
72	Kakamega	t	KKM	\N
73	Nakuru	t	NAK	\N
74	Meru	t	MER	\N
75	Embu	t	EMB	\N
76	Muranga	t	MUR	\N
77	Thika	t	TKA	\N
78	Machakos	t	MKS	\N
79	Kiambu	t	KMB	\N
80	Nyahururu	t	NYU	\N
81	Kericho	t	KER	\N
82	Eldoret	t	ELD	\N
83	Kitale	t	KIT	\N
84	Bungoma	t	BGM	\N
85	Kisii	t	KIS	\N
86	Kisumu	t	KSM	\N
87	Nyeri	t	NYR	\N
88	Naivasha	t	NAV	\N
89	ENERGY AND PETROLEUM TRIBUNAL	f	EPTBN	\N
90	Commercial Suit Division	t	MCCOMMSU	\N
91	Small Claims Court	f	SCC	\N
92	Garissa	t	GAR	\N
93	Lamu	t	LAM	\N
94	Judiciary Training Institute	f	JTI	\N
95	Administration	f	ADMIN	\N
96	Judiciary Committee on Elections	t	JCE	\N
\.


--
-- Data for Name: statistics_financialquarter; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_financialquarter (id, name, start_date, end_date, quarter_number, financial_year_id) FROM stdin;
1	Q1	2024-07-01	2024-09-30	1	1
2	Q2	2024-10-01	2024-12-31	2	1
3	Q3	2025-01-01	2025-03-31	3	1
4	Q4	2025-04-01	2025-06-30	4	1
\.


--
-- Data for Name: statistics_financialyear; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_financialyear (id, name, start_date, end_date) FROM stdin;
1	2024/2025	2024-07-01 00:00:00+00	2025-06-30 00:00:00+00
\.


--
-- Data for Name: statistics_months; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_months (id, name, month_number, financial_quarter) FROM stdin;
1	January	31	3
2	February	28	3
3	March	31	3
4	April	30	4
5	May	31	4
6	June	30	4
7	July	31	1
8	August	31	1
9	September	30	1
10	October	31	2
11	November	30	2
12	December	31	2
\.


--
-- Data for Name: statistics_unit; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_unit (id, name, unique_id, unique_code, head_id_fk, subhead_id_fk, has_division, is_court, latitude, longitude, unit_rank_id, is_template, template_unit_id, dcrt_unique_id) FROM stdin;
338	Refugee Appeal Board	RABD	RABD	8	136	f	f	0	0	7	f	\N	Refugee Appeal Board
343	Insurance Appeals Tribunal 	IATT	IATT	8	136	f	f	0	0	7	f	\N	Insurance Appeals Tribunal 
384	Judiciary Committee on Elections	JCE	JCE	9	2	f	f	0	0	8	f	\N	Judiciary Committee on Elections
14	Malindi Court of Appeal	MLDCOA	MLDCOA	2	5	f	f	0	0	2	f	\N	32005
21	Garsen High Court	GSNHGC	GSNHGC	3	14	f	f	0	0	3	f	\N	43036
31	Voi High Court	VOIHGC	VOIHGC	3	41	f	f	0	0	3	f	\N	63035
16	Malindi Environment and Land Court	MLDELC	MLDELC	5	5	f	f	0	0	5	f	\N	Malindi Environment and Land Court
68	Meru Environment and Land Court	MRUELC	MRUELC	5	30	f	f	0	0	5	f	\N	Meru Environment and Land Court
75	Chuka Environment and Land Court	CKAELC	CKAELC	5	10	f	f	0	0	5	f	\N	Chuka Environment and Land Court
9	Mombasa Kadhi Court	MSAKDC	MSAKDC	7	32	f	f	0	0	6	f	\N	17017
10	Mariakani Kadhi Court	MRKKDC	MRKKDC	7	84	f	f	0	0	6	f	\N	17039
12	Kwale Kadhi Court	KWLKDC	KWLKDC	7	75	f	f	0	0	6	f	\N	27015
13	Msambweni Kadhi Court	MWNKDC	MWNKDC	7	133	f	f	0	0	6	f	\N	27041
19	Kilifi Kadhi Court	KLFKDC	KLFKDC	7	71	f	f	0	0	6	f	\N	37014
20	Malindi Kadhi Court	MLDKDC	MLDKDC	7	5	f	f	0	0	6	f	\N	37016
25	Garsen Kadhi Court	GSNKDC	GSNKDC	7	14	f	f	0	0	6	f	\N	47025
26	Hola Kadhi Court	HLAKDC	HLAKDC	7	54	f	f	0	0	6	f	\N	47026
30	Lamu Kadhi Court	LMUKDC	LMUKDC	7	77	f	f	0	0	6	f	\N	57027
35	Voi Kadhi Court	VOIKDC	VOIKDC	7	41	f	f	0	0	6	f	\N	67018
38	Modogashe Kadhi Court	MDGMGC	MDGMGC	7	144	f	f	0	0	6	f	\N	Modogashe Kadhi Court
42	Garissa Kadhi Court	GRSKDC	GRSKDC	7	13	f	f	0	0	6	f	\N	77024
44	Ijara Kadhi Court	IJRKDC	IJRKDC	7	131	f	f	0	0	6	f	\N	77034
45	Balambala Kadhi Court	BLMKDC	BLMKDC	7	123	f	f	0	0	6	f	\N	77044
47	Wajir Kadhi Court	WJRKDC	WJRKDC	7	118	f	f	0	0	6	f	\N	87030
48	Habaswein Kadhi Court	HBSKDC	HBSKDC	7	130	f	f	0	0	6	f	\N	87033
49	Bute Kadhi Court	BTEKDC	BTEKDC	7	124	f	f	0	0	6	f	\N	87037
50	Eldas Kadhi Court	EDSKDC	EDSKDC	7	126	f	f	0	0	6	f	\N	87038
52	Mandera Kadhi Court	MNDKDC	MNDKDC	7	82	f	f	0	0	6	f	\N	97028
53	Elwak Kadhi Court	EWKKDC	EWKKDC	7	127	f	f	0	0	6	f	\N	97035
54	Takaba Kadhi Court	TKBKDC	TKBKDC	7	134	f	f	0	0	6	f	\N	97036
60	Moyale Kadhi Court	MYLKDC	MYLKDC	7	91	f	f	0	0	6	f	\N	107006
64	Isiolo Kadhi Court	ISLKDC	ISLKDC	7	55	f	f	0	0	6	f	\N	117004
66	Merti Kadhi Court	MRTKDC	MRTKDC	7	132	f	f	0	0	6	f	\N	117043
61	Sereolipi Kadhi Court	SERKDC	SERKDC	7	55	f	f	0	0	6	f	\N	Sereolipi Kadhi Court
36	Garissa High Court	GRSHGC	GRSHGC	3	13	f	f	0	0	3	f	\N	73033
80	Embu Environment and Land Court	EMBELC	EMBELC	5	12	f	f	0	0	5	f	\N	Embu Environment and Land Court
100	Makueni Environment and Land Court	MKNELC	MKNELC	5	28	f	f	0	0	5	f	\N	Makueni Environment and Land Court
90	Kitui Kadhi Court	KTIKDC	KTIKDC	7	25	f	f	0	0	6	f	\N	157031
98	Machakos Kadhi Court	MKSKDC	MKSKDC	7	27	f	f	0	0	6	f	\N	167009
114	Nyeri Kadhi Court	NYRKDC	NYRKDC	7	6	f	f	0	0	6	f	\N	197008
116	Kerugoya Environment and Land Court	KRGELC	KRGELC	5	21	f	f	0	0	5	f	\N	Kerugoya Environment and Land Court
78	Maua Kadhi court	MUAKDC	MUAKDC	7	87	f	f	0	0	6	f	\N	127045
127	Muranga Kadhi Court	MRGKDC	MRGKDC	7	33	f	f	0	0	6	f	\N	217007
91	Mwingi Kadhi Court 	MWGKDC	MWGKDC	7	96	f	f	0	0	6	f	\N	Mwingi Kadhi Court 
154	Eldoret Kadhi Court	ELDKDC	ELDKDC	7	11	f	f	0	0	6	f	\N	277011
245	Nairobi Employment and Labour Relations Court	NRBERC	NRBERC	4	3	f	f	0	0	4	f	\N	474017
5	Mariakani Magistrate Court	MRKMGC	MRKMGC	6	84	f	f	0	0	6	f	\N	16068
83	Siakago Magistrate Court	SKGMGC	SKGMGC	6	108	f	f	0	0	6	f	\N	146044
86	Kitui Magistrate Court	KTIMGC	KTIMGC	6	25	f	f	0	0	6	f	\N	156112
87	Kyuso Magistrate Court	KYSMGC	KYSMGC	6	76	f	f	0	0	6	f	\N	156113
88	Mutomo Magistrate Court	MTMMGC	MTMMGC	6	95	f	f	0	0	6	f	\N	Mutomo Magistrate Court
94	Kangundo Magistrate Court	KGDMGC	KGDMGC	6	62	f	f	0	0	6	f	\N	166035
95	Machakos Magistrate Court	MKSMGC	MKSMGC	6	27	f	f	0	0	6	f	\N	166038
96	Mavoko Magistrate Court	MVKMGC	MVKMGC	6	88	f	f	0	0	6	f	\N	166085
102	Makueni Magistrate Court	MKNMGC	MKNMGC	6	28	f	f	0	0	6	f	\N	176037
103	Makindu Magistrate Court	MDUMGC	MDUMGC	6	81	f	f	0	0	6	f	\N	176039
104	Tawa Magistrate Court	TWAMGC	TWAMGC	6	113	f	f	0	0	6	f	\N	176045
110	Karatina Magistrate Court	KTNMGC	KTNMGC	6	64	f	f	0	0	6	f	\N	196019
111	Mukurwe-ini Magistrate Court	MKWMGC	MKWMGC	6	93	f	f	0	0	6	f	\N	196025
112	Nyeri Magistrate Court	NYRMGC	NYRMGC	6	6	f	f	0	0	6	f	\N	196028
119	Gichugu Magistrate Court	GCGMGC	GCGMGC	6	50	f	f	0	0	6	f	\N	206015
120	Kerugoya Magistrate Court	KRGMGC	KRGMGC	6	21	f	f	0	0	6	f	\N	206036
123	Kandara Magistrate Court	KNDMGC	KNDMGC	6	60	f	f	0	0	6	f	\N	216017
32	Taveta Magistrate Court	TVTMGC	TVTMGC	6	112	f	f	0	0	6	f	\N	66071
71	Nkubu Magistrate Court	NKBMGC	NKBMGC	6	99	f	f	0	0	6	f	\N	126042
72	Tigania Magistrate Court	TGAMGC	TGAMGC	6	114	f	f	0	0	6	f	\N	126046
166	Nakuru ELRC	NKRERC	NKRERC	4	35	f	f	0	0	4	f	\N	324028
181	Kericho ELRC	KRCERC	KRCERC	4	20	f	f	0	0	4	f	\N	354025
179	Kajiado Kadhi Court	KJDKDC	KJDKDC	7	17	f	f	0	0	6	f	\N	347019
184	Kericho Kadhi Court	KRCKDC	KRCKDC	7	20	f	f	0	0	6	f	\N	357040
149	Kitale Kadhi Court	KTGKDC	KTGKDC	7	24	f	f	0	0	6	f	\N	267012
141	Lodwar Kadhi Court	LDWKDC	LDWKDC	7	26	f	f	0	0	6	f	\N	Lodwar Kadhi Court
194	Kakamega Kadhi Court	KKGKDC	KKGKDC	7	18	f	f	0	0	6	f	\N	377001
204	Bungoma Kadhi Court	BNGKDC	BNGKDC	7	8	f	f	0	0	6	f	\N	397010
221	Kisumu Kadhi Court	KSMKDC	KSMKDC	7	4	f	f	0	0	6	f	\N	427002
167	Nakuru Environment and Land Court	NKRELC	NKRELC	5	35	f	f	0	0	5	f	\N	Nakuru Environment and Land Court
182	Kericho Environment and Land Court	KRCELC	KRCELC	5	20	f	f	0	0	5	f	\N	Kericho Environment and Land Court
189	Kakamega Environment and Land Court	KKGELC	KKGELC	5	18	f	f	0	0	5	f	\N	Kakamega Environment and Land Court
162	Nanyuki Magistrate Court	NYKMGC	NYKMGC	6	36	f	f	0	0	6	f	\N	316027
163	Nyahururu Magistrate Court	NYHMGC	NYHMGC	6	100	f	f	0	0	6	f	\N	316090
169	Molo Magistrate Court	MOLMGC	MOLMGC	6	90	f	f	0	0	6	f	\N	326086
170	Naivasha Magistrate Court	NSHMGC	NSHMGC	6	34	f	f	0	0	6	f	\N	326087
171	Nakuru Magistrate Court	NKRMGC	NKRMGC	6	35	f	f	0	0	6	f	\N	326088
174	Narok Magistrate Court	NRKMGC	NRKMGC	6	37	f	f	0	0	6	f	\N	336089
177	Kajiado Magistrate Court	KJDMGC	KJDMGC	6	17	f	f	0	0	6	f	\N	346079
178	Loitoktok Magistrate Court	LTKMGC	LTKMGC	6	79	f	f	0	0	6	f	\N	348022
186	Bomet Magistrate Court	BMTMGC	BMTMGC	6	7	f	f	0	0	6	f	\N	366075
190	Butali Magistrate Court	BTLMGC	BTLMGC	6	45	f	f	0	0	6	f	\N	376003
144	Wamba under Maralal Magistrate Court	WMBMGC	WMBMGC	6	83	f	f	0	0	6	f	\N	258008
137	Lokichar under Lodwar Magistrate Court	LKCMGC	LKCMGC	6	26	f	f	0	0	6	f	\N	238013
138	Lokitaung under Lodwar Magistrate Court	LKTMGC	LKTMGC	6	26	f	f	0	0	6	f	\N	238014
192	Kakamega Magistrate Court	KKGMGC	KKGMGC	6	18	f	f	0	0	6	f	\N	376005
34	Wundanyi Magistrate Court	WDYMGC	WDYMGC	6	122	f	f	0	0	6	f	\N	66074
41	Garissa Magistrate Court	GRSMGC	GRSMGC	6	13	f	f	0	0	6	f	\N	76108
57	Moyale Magistrate Court	MYLMGC	MYLMGC	6	91	f	f	0	0	6	f	\N	106022
73	Githongo Magistrate Court	GTGMGC	GTGMGC	6	51	f	f	0	0	6	f	\N	126048
286	Eldoret ELRC	ELDELRC	ELDELRC	4	11	f	f	0	0	4	f	\N	274034
258	Political Parties Disputes Tribunal (PPDT)	PPDTBN	PPDTBN	8	136	f	f	0	0	7	f	\N	Political Parties Disputes Tribunal (PPDT)
259	The National Environment Tribunal	NETTBN	NETTBN	8	136	f	f	0	0	7	f	\N	The National Environment Tribunal
261	Co-operative Tribunal	COPTBN	COPTBN	8	136	f	f	0	0	7	f	\N	Co-operative Tribunal
264	HIV and AIDS Tribunal	HIVTBN	HIVTBN	8	136	f	f	0	0	7	f	\N	HIV and AIDS Tribunal
266	Rent Restriction Tribunal	RRTTBN	RRTTBN	8	136	f	f	0	0	7	f	\N	Rent Restriction Tribunal
255	Nairobi Kadhi Court	NRBKDC	NRBKDC	7	2	f	f	0	0	6	f	\N	477003
256	Kibera Kadhi Court	KBRKDC	KBRKDC	7	67	f	f	0	0	6	f	\N	477022
328	Kakuma Kadhi Court	KKMKDC	KKMKDC	7	58	f	f	0	0	6	f	\N	237013
326	Bura/Fafi Kadhis Court	BAFKDC	BAFKDC	7	143	f	f	0	0	6	f	\N	Bura/Fafi Kadhis Court
327	Witu Kadhi Court	WITKDC	WITKDC	7	135	f	f	0	0	6	f	\N	Witu Kadhi Court
235	Kisii Environment and Land Court	KISELC	KISELC	5	23	f	f	0	0	5	f	\N	Kisii Environment and Land Court
281	Industrial Property Tribunal	IPT	IPT	8	136	f	f	0	0	7	f	\N	Industrial Property Tribunal
307	Transport Licensing Appeals Board Tribunal	TLBTBN	TLBTBN	8	136	f	f	0	0	7	f	\N	Transport Licensing Appeals Board Tribunal
310	Legal Education Appeals Tribunal 	LEAT	LEAT	8	136	f	f	0	0	7	f	\N	Legal Education Appeals Tribunal 
311	Micro and Small Enterprise Tribunal 	MSET	MSET	8	136	f	f	0	0	7	f	\N	Micro and Small Enterprise Tribunal 
246	Milimani Environment and Land Court	MILELC	MILELC	5	2	f	f	0	0	5	f	\N	Milimani Environment and Land Court
287	Migori ELC	MGRELC	MGRELC	5	31	f	f	0	0	5	f	\N	445063
289	Muranga ELC	MRGELC	MRGELC	5	33	f	f	0	0	5	f	\N	215065
294	Thika Environment and Land Court	TKAELC	TKAELC	5	42	f	f	0	0	5	f	\N	Thika Environment and Land Court
301	Nyahururu ELC	NYHELC	NYHELC	5	100	f	f	0	0	5	f	\N	Nyahururu ELC
317	Narok ELC	NRKELC	NRKELC	5	37	f	f	0	0	5	f	\N	335067
227	Mbita Magistrate Court	MBTMGC	MBTMGC	6	89	f	f	0	0	6	f	\N	436107
230	Kehancha Magistrate Court	KHCMGC	KHCMGC	6	65	f	f	0	0	6	f	\N	446095
232	Rongo Magistrate Court	RNGMGC	RNGMGC	6	105	f	f	0	0	6	f	\N	446105
237	Ogembo Magistrate Court	OGBMGC	OGBMGC	6	102	f	f	0	0	6	f	\N	456103
58	Marsabit Magistrate Court	MSBMGC	MSBMGC	6	29	f	f	0	0	6	f	\N	106024
63	Isiolo Magistrate Court	ISLMGC	ISLMGC	6	55	f	f	0	0	6	f	\N	116016
69	Maua Magistrate Court	MUAMGC	MUAMGC	6	87	f	f	0	0	6	f	\N	126032
263	Water Appeals Board	WAB	ALBTBN	8	136	f	f	0	0	7	f	\N	Water Appeals Board
277	Standards Tribunal	STDTBN	STDTBN	8	136	f	f	0	0	7	f	\N	Standards Tribunal
283	Registrar of Trademark Tribunal	RTT	RTT	8	136	f	f	0	0	7	f	\N	Registrar of Trademark Tribunal
318	Narok Kadhi Court	NRKKC	NRKKC	7	37	f	f	0	0	6	f	\N	Narok Kadhi Court
305	Northhorr/Illeret Kadhi Court Under Marsabit Law Court	NTHKDC	NTHKDC	7	29	f	f	0	0	6	f	\N	Northhorr/Illeret Kadhi Court Under Marsabit Law Court
265	Public Private Partnership Petition Committee	PPPPC	PPPPC	8	136	f	f	0	0	7	f	\N	Public Private Partnership Petition Committee
293	Land Dispute Tribunal	LDT	LDT	8	136	f	f	0	0	7	f	\N	Land Dispute Tribunal
336	Meru Kadhi Court	MRUKDC	MRUKDC	7	30	f	f	0	0	6	f	\N	Meru Kadhi Court
330	Copyright Tribunal	COPT	COPT	8	156	f	f	0	0	7	f	\N	Copyright Tribunal
276	Competition Tribunal	CPTTBN	CPTTBN	8	136	f	f	0	0	7	f	\N	Competition Tribunal
262	Auctioneers Licensing Board	ALB	ALB	8	136	f	f	0	0	7	f	\N	Auctioneers Licensing Board
347	Kilgoris ELC	KILELC	KILELC	5	70	f	f	0	0	5	f	\N	Kilgoris ELC
371	Siaya ELC	SYAELC	SYAELC	5	40	f	f	0	0	5	f	\N	Siaya ELC
372	Nyamira Environment and Land Court	NYMELC	NYMELC	5	38	f	f	0	0	5	f	\N	Nyamira Environment and Land Court
374	Nanyuki Environment and Land Court	NYKELC	NYKELC	5	36	f	f	0	0	5	f	\N	Nanyuki Environment and Land Court
376	Kitui Environment and Land Court	KTIELC	KTIELC	5	25	f	f	0	0	5	f	\N	Kitui Environment and Land Court
377	Kwale Environment and Land Court	KWLELC	KWLELC	5	75	f	f	0	0	5	f	\N	Kwale Environment and Land Court
379	Homabay Environment and Land Court	HMBELC	HMBELC	5	15	f	f	0	0	5	f	\N	Homabay Environment and Land Court
76	Chuka Magistrate Court	CKAMGC	CKAMGC	6	10	f	f	0	0	6	f	\N	136033
4	Kaloleni Magistrate Court	KLNMGC	KLNMGC	6	59	f	f	0	0	6	f	\N	16063
22	Kipini under Garsen Magistrate Court	KPNMGC	KPNMGC	6	14	f	f	0	0	6	f	\N	48037
124	Kangema Magistrate Court	KNGMGC	KNGMGC	6	61	f	f	0	0	6	f	\N	216018
342	Timau Mobile Court under Meru Law Courts	TIMMGC	TIMMGC	6	30	f	f	0	0	6	f	\N	Timau Mobile Court under Meru Law Courts
140	Kakuma Magistrate Court	KKMMGC	KKMMGC	6	58	f	f	0	0	6	f	\N	236062
145	Maralal Magistrate Court	MRLMGC	MRLMGC	6	83	f	f	0	0	6	f	\N	256023
148	Kitale Magistrate Court	KTGMGC	KTGMGC	6	24	f	f	0	0	6	f	\N	266057
153	Eldoret Magistrate Court	ELDMGC	ELDMGC	6	11	f	f	0	0	6	f	\N	276050
82	Runyenjes Magistrate Court	RNJGMC	RNJGMC	6	106	f	f	0	0	6	f	\N	146043
155	Iten Magistrate Court	ITNMGC	ITNMGC	6	56	f	f	0	0	6	f	\N	286052
193	Mumias Magistrate Court	MMSMGC	MMSMGC	6	94	f	f	0	0	6	f	\N	376009
356	Office of the Registrar Magistrate Court (ORMC)	ORMC	ORMC	12	1	f	f	0	0	12	f	\N	Office of the Registrar Magistrate Court (ORMC)
358	Office of Registrar Court of Appeal (ORCOA)	ORCOA	ORCOA	12	1	f	f	0	0	12	f	\N	Office of Registrar Court of Appeal (ORCOA)
359	Office of Registrar High Court (ORHC)	ORHC	ORHC	12	2	f	f	0	0	12	f	\N	Office of Registrar High Court (ORHC)
362	Office of Registrar Environment and Land Court (ORELC)	ORELC	ORELC	12	2	f	f	0	0	12	f	\N	Office of Registrar Environment and Land Court (ORELC)
363	Office of Registrar Tribunals (ORTR)	ORTR	ORTR	12	1	f	f	0	0	12	f	\N	Office of Registrar Tribunals (ORTR)
364	Office of Registrar Small Claims Court (ORSCC)	ORSCC	ORSCC	12	3	f	f	0	0	12	f	\N	Office of Registrar Small Claims Court (ORSCC)
386	Directorate of Planning and Organisational Performance	DPOP	DPOP	11	2	f	f	0	0	11	f	\N	Directorate of Planning and Organisational Performance
387	Finance and Accounts	FA	FA	11	2	f	f	0	0	11	f	\N	Finance and Accounts
388	Supply Chain Management	SCM	SCM	11	2	f	f	0	0	11	f	\N	Supply Chain Management
390	Public Affairs and Communication	PAC	PAC	11	2	f	f	0	0	11	f	\N	Public Affairs and Communication
392	Information Communication Technology	ICT	ICT	11	2	f	f	0	0	11	f	\N	Information Communication Technology
367	Office of The Judiciary Ombudsman (OJO)	OJO	OJO	11	1	f	f	0	0	11	f	\N	Office of The Judiciary Ombudsman (OJO)
340	HIV Tribunal	HAT	HAT	8	155	f	f	0	0	7	f	\N	HIV Tribunal
348	ENERGY AND PETROLEUM TRIBUNAL	EPTBN	EPTBN	8	136	f	f	0	0	7	f	\N	ENERGY AND PETROLEUM TRIBUNAL
312	Competent Authority Tribunal 	COMPTBN	COMPTBN	8	136	f	f	0	0	7	f	\N	Competent Authority Tribunal 
43	Dadaab Kadhi Court	DDBKDC	DDBKDC	7	125	f	f	0	0	6	f	\N	Dadaab Kadhi Court
59	Marsabit Kadhi Court	MSBKDC	MSBKDC	7	29	f	f	0	0	6	f	\N	107005
65	Garbatulla Kadhi Court	GBTKDC	GBTKDC	7	129	f	f	0	0	6	f	\N	117042
3	Mombasa Environment and Land Court	MSAELC	MSAELC	5	32	f	f	0	0	5	f	\N	Mombasa Environment and Land Court
37	Garissa Environment and Land Court	GRSELC	GRSELC	5	13	f	f	0	0	5	f	\N	Garissa Environment and Land Court
93	Machakos Environment and Land Court 	MKSELC	MKSELC	5	27	f	f	0	0	5	f	\N	Machakos Environment and Land Court 
109	Nyeri Environment and Land Court	NYRELC	NYRELC	5	6	f	f	0	0	5	f	\N	Nyeri Environment and Land Court
126	Muranga Magistrate Court	MRGMGC	MRGMGC	6	33	f	f	0	0	6	f	\N	216026
129	Kiambu Magistrate Court	KMBMGC	KMBMGC	6	22	f	f	0	0	6	f	\N	226081
132	Gatundu Magistrate Court	GTDMGC	GTDMGC	6	49	f	f	0	0	6	f	\N	226093
306	Vihiga Kadhi Court	VHGKDC	VHGKDC	6	117	f	f	0	0	6	f	\N	Vihiga Kadhi Court
56	Laisamis/Loyangalani Magistrate Court under Marsabit Law Court	LSMMGC	LSMMGC	6	29	f	f	0	0	6	f	\N	Laisamis/Loyangalani Magistrate Court under Marsabit Law Court
101	Kilungu Magistrate Court	KGUMGC	KGUMGC	6	72	f	f	0	0	6	f	\N	Kilungu Magistrate Court
334	Etago Mobile Court under Ogembo Court	ETGMGC	ETGMGC	6	102	f	f	0	0	6	f	\N	Etago Mobile Court under Ogembo Court
304	Northhorr/Illeret Magistrate Court Under Marsabit Law Court	NTHMGC	NTHMGC	6	29	f	f	0	0	6	f	\N	Northhorr/Illeret Magistrate Court Under Marsabit Law Court
7	Shanzu Magistrate Court	SNZMGC	SNZMGC	6	107	f	f	0	0	6	f	\N	16070
11	Kwale Magistrate Court	KWLMGC	KWLMGC	6	75	f	f	0	0	6	f	\N	26065
18	Malindi Magistrate Court	MLDMGC	MLDMGC	6	5	f	f	0	0	6	f	\N	36067
200	Bungoma Magistrate Court	BNGMGC	BNGMGC	6	8	f	f	0	0	6	f	\N	396049
369	Community Service Orders Co-ordinator (CSOC)	CSOC	CSOC	12	1	f	f	0	0	12	f	\N	Community Service Orders Co-ordinator (CSOC)
365	Office of Registrar Judicial Service Commission (ORJSC)	ORJSC	ORJSC	12	1	f	f	0	0	12	f	\N	Office of Registrar Judicial Service Commission (ORJSC)
366	Office of The Chief Justice (OCJ)	OCJ	OCJ	12	1	f	f	0	0	12	f	\N	Office of The Chief Justice (OCJ)
394	Administration and Security Services	ASS	ASS	11	2	f	f	0	0	11	f	\N	Administration and Security Services
201	Kimilili Magistrate Court	KMLMGC	KMLMGC	6	73	f	f	0	0	6	f	\N	396056
202	Sirisia Magistrate Court	SRSMGC	SRSMGC	6	109	f	f	0	0	6	f	\N	396059
207	Busia Magistrate Court	BSAMGC	BSAMGC	6	9	f	f	0	0	6	f	\N	406002
397	Library	Library	Library	11	2	f	f	0	0	11	f	\N	Library
260	Sports Disputes Tribunal	SPDTBN	SPDTBN	8	136	f	f	0	0	7	f	\N	Sports Disputes Tribunal
267	Business Premises Rent Tribunal	BPRTBN	BPRTBN	8	136	f	f	0	0	7	f	\N	Business Premises Rent Tribunal
309	Communications and Multimedia Appeals Tribunal 	CAMAT	CAMAT	8	136	f	f	0	0	7	f	\N	Communications and Multimedia Appeals Tribunal 
282	State Corporations Appeal Tribunal	SCAT	SCAT	8	136	f	f	0	0	7	f	\N	State Corporations Appeal Tribunal
280	National Civil Aviation Administrative Review Tribunal	NAART	NAART	8	136	f	f	0	0	7	f	\N	National Civil Aviation Administrative Review Tribunal
308	Advocates Disciplinary Tribunal	ADT	ADT	8	136	f	f	0	0	7	f	\N	Advocates Disciplinary Tribunal
303	Laisamis/Loyangalani Kadhi Court under Marsabit Law Court	LSMKDC	LSMKDC	7	29	f	f	0	0	6	f	\N	Laisamis/Loyangalani Kadhi Court under Marsabit Law Court
172	Nakuru Kadhi Court	NKRKDC	NKRKDC	7	35	f	f	0	0	6	f	\N	327020
315	Kenya Institute of Supplies Management Elections Committee	KISM	KISM	9	141	f	f	0	0	8	f	\N	Kenya Institute of Supplies Management Elections Committee
135	Thika Kadhi Court	TKAKDC	TKAKDC	7	42	f	f	0	0	6	f	\N	227029
228	Homabay Kadhi Court	HMBKDC	HMBKDC	7	15	f	f	0	0	6	f	\N	437021
233	Migori Kadhi Court	MGRKDC	MGRKDC	7	31	f	f	0	0	6	f	\N	447023
292	Busia Kadhi Court	BSAKDC	BSAKDC	7	9	f	f	0	0	6	f	\N	407048
147	Kitale Environment and Land Court	KTGELC	KTGELC	5	24	f	f	0	0	5	f	\N	Kitale Environment and Land Court
152	Eldoret Environment and Land Court	ELDELC	ELDELC	5	11	f	f	0	0	5	f	\N	Eldoret Environment and Land Court
198	Bungoma  Environment and Land Court	BNGELC	BNGELC	5	8	f	f	0	0	5	f	\N	Bungoma  Environment and Land Court
206	Busia Environment and Land Court	BSAELC	BSAELC	5	9	f	f	0	0	5	f	\N	Busia Environment and Land Court
215	Kisumu Environment and Land Court	KSMELC	KSMELC	5	4	f	f	0	0	5	f	\N	Kisumu Environment and Land Court
288	Kajiado ELC	KJDELC	KJDELC	5	17	f	f	0	0	5	f	\N	345062
133	Githunguri Magistrate Court	GTNMGC	GTNMGC	6	52	f	f	0	0	6	f	\N	226094
134	Thika Magistrate Court	TKAMGC	TKAMGC	6	42	f	f	0	0	6	f	\N	226118
353	Milimani Small Claims Court	MSCC	MSCC	13	3	f	f	0	0	13	f	\N	Milimani Small Claims Court
139	Lodwar Magistrate Court	LDWMGC	LDWMGC	6	26	f	f	0	0	6	f	\N	236055
196	Hamisi Magistrate Court	HMSMGC	HMSMGC	6	53	f	f	0	0	6	f	\N	386051
209	Bondo Magistrate Court	BNDMGC	BNDMGC	6	44	f	f	0	0	6	f	\N	416001
210	Siaya Magistrate Court	SYAMGC	SYAMGC	6	40	f	f	0	0	6	f	\N	416010
216	Kisumu Magistrate Court	KSMMGC	KSMMGC	6	4	f	f	0	0	6	f	\N	426006
217	Maseno Magistrate Court	MSNMGC	MSNMGC	6	86	f	f	0	0	6	f	\N	426007
218	Winam Magistrate Court	WNMMGC	WNMMGC	6	121	f	f	0	0	6	f	\N	426013
160	Kabarnet Magistrate Court	KBTMGC	KBTMGC	6	16	f	f	0	0	6	f	\N	306078
220	Tamu Magistrate Court	TAMMGC	TAMMGC	6	111	f	f	0	0	6	f	\N	426106
325	Kahawa Magistrate Court	KHWMGC	KHWMGC	6	142	f	f	0	0	6	f	\N	Kahawa Magistrate Court
331	Baragoi Mobile Court (under Maralal Magistrate Court)	BRGMGC	BRGMGC	6	83	f	f	0	0	6	f	\N	Baragoi Mobile Court (under Maralal Magistrate Court)
300	Migwani Mobile Court Under Mwingi Law Court	MGWMGC	MGWMGC	6	96	f	f	0	0	6	f	\N	Migwani Mobile Court Under Mwingi Law Court
157	Kapsabet Magistrate Court	KPBMGC	KPBMGC	6	63	f	f	0	0	6	f	\N	296054
252	Kibera Magistrate Court	KBRMGC	KBRMGC	6	67	f	f	0	0	6	f	\N	476082
254	JKIA Magistrate Court	JKAMGC	JKAMGC	6	57	f	f	0	0	6	f	\N	476121
357	Office of Registrar Supreme Court (ORSC)	ORSC	ORSC	12	1	f	f	0	0	12	f	\N	Office of Registrar Supreme Court (ORSC)
361	Office of Registrar Employment and Labour Relations Court (ORELRC)	ORELRC	ORELRC	12	3	f	f	0	0	12	f	\N	Office of Registrar Employment and Labour Relations Court (ORELRC)
368	Office of The Chief Registrar Judiciary (OCRJ)	OCRJ	OCRJ	12	1	f	f	0	0	12	f	\N	Office of The Chief Registrar Judiciary (OCRJ)
375	Kapsabet Environment and Land Court	KPBELC	KPBELC	5	63	f	f	0	0	5	f	\N	Kapsabet Environment and Land Court
67	Meru High Court	MRUHGC	MRUHGC	3	30	f	f	0	0	3	f	\N	123014
355	Judiciary Training Institute	JTI	JTI	11	1	f	f	0	0	11	f	\N	Judiciary Training Institute
389	Building Services	BS	BS	11	2	f	f	0	0	11	f	\N	Building Services
391	Internal Audit and Risk Management	IAM	IAM	11	2	f	f	0	0	11	f	\N	Internal Audit and Risk Management
92	Machakos High Court	MKSHGC	MKSHGC	3	27	f	f	0	0	3	f	\N	163013
378	Vihiga Environment and Land Court	VHGELC	VHGELC	5	117	f	f	0	0	5	f	\N	Vihiga Environment and Land Court
360	Office of Principal Judge (OPJ)	OPJ	OPJ	12	2	f	f	0	0	12	f	\N	Office of Principal Judge (OPJ)
393	Human Resource Management	HRM	HRM	11	2	f	f	0	0	11	f	\N	Human Resource Management
396	The National Council for the Administration of Justice	NCAJ	NCAJ	11	2	f	f	0	0	11	f	\N	The National Council for the Administration of Justice
339	Education Appeals Tribunal - Nairobi	EATNAIROBI	EATNAIROBI	8	154	f	f	0	0	7	f	\N	Education Appeals Tribunal - Nairobi
383	Disciplinary & Ethics Committee of the Medical Practitioners and Dentists Council	DECMPDC	DECMPDC	8	136	f	f	0	0	7	f	\N	Disciplinary & Ethics Committee of the Medical Practitioners and Dentists Council
106	Nyeri Court of Appeal	NYRCOA	NYRCOA	2	6	f	f	0	0	2	f	\N	192002
150	Eldoret Court of Appeal	ELDCOA	ELDCOA	2	11	f	f	0	0	2	f	\N	Eldoret Court of Appeal
373	Isiolo Environment and Land Court	ISLELC	ISLELC	5	55	f	f	0	0	5	f	\N	Isiolo Environment and Land Court
239	Keroka Magistrate Court	KRKMGC	KRKMGC	6	66	f	f	0	0	6	f	\N	466096
332	Mikinduri Mobile Court Under Tigania	MIKMGC	MIKMGC	6	114	f	f	0	0	6	f	\N	Mikinduri Mobile Court Under Tigania
226	Oyugis Magistrate Court	OYGMGC	OYGMGC	6	104	f	f	0	0	6	f	\N	436104
345	Kikima Magistrate Court Under Tawa Law Courts	KIKMGC	KIKMGC	6	113	f	f	0	0	6	f	\N	Kikima Magistrate Court Under Tawa Law Courts
322	Nakuru Court of Appeal	NKRCOA	NKRCOA	2	35	f	f	0	0	2	f	\N	Nakuru Court of Appeal
323	Mombasa Court of Appeal	MSACOA	MSACOA	2	32	f	f	0	0	2	f	\N	Mombasa Court of Appeal
243	Nairobi Court of Appeal	NRBCOA	NRBCOA	2	1	f	f	0	0	2	f	\N	472004
175	Kajiado High Court	KJDHGC	KJDHGC	3	17	f	f	0	0	3	f	\N	343051
185	Bomet High Court	BMTHGC	BMTHGC	3	7	f	f	0	0	3	f	\N	363052
188	Kakamega High Court	KKGHGC	KKGHGC	3	18	f	f	0	0	3	f	\N	373003
197	Bungoma High Court	BNGHGC	BNGHGC	3	8	f	f	0	0	3	f	\N	393015
205	Busia High Court	BSAHGC	BSAHGC	3	9	f	f	0	0	3	f	\N	403001
229	Migori High Court	MGRHGC	MGRHGC	3	31	f	f	0	0	3	f	\N	443032
234	Kisii High Court	KISHGC	KISHGC	3	23	f	f	0	0	3	f	\N	453031
238	Nyamira High Court	NYMHGC	NYMHGC	3	38	f	f	0	0	3	f	\N	463059
278	Thika High Court	TKAHGC	TKAHGC	3	42	f	f	0	0	3	f	\N	Thika High Court
244	Milimani High Court	MILHGC	MILHGC	3	2	f	f	0	0	3	f	\N	Milimani High Court
15	Malindi High Court	MLDHGC	MLDHGC	3	5	f	f	0	0	3	f	\N	33020
55	Marsabit High Court	MSBHGC	MSBHGC	3	29	f	f	0	0	3	f	\N	103037
74	Chuka High Court	CKAHGC	CKAHGC	3	10	f	f	0	0	3	f	\N	133039
79	Embu High Court	EMBHGC	EMBHGC	3	12	f	f	0	0	3	f	\N	143010
84	Kitui High Court	KTIHGC	KTIHGC	3	25	f	f	0	0	3	f	\N	153041
136	Lodwar High Court	LDWHGC	LDWHGC	3	26	f	f	0	0	3	f	\N	233045
302	Nyahururu High Court	NYHHGC	NYHHGC	3	100	f	f	0	0	3	f	\N	Nyahururu High Court
257	Wajir High Court	WJRHGC	WJRHGC	3	118	f	f	0	0	3	f	\N	Wajir High Court
158	Kabarnet High Court	KBTHGC	KBTHGC	3	16	f	f	0	0	3	f	\N	303049
161	Nanyuki High Court	NYKHGC	NYKHGC	3	36	f	f	0	0	3	f	\N	313050
165	Nakuru High Court	NKRHGC	NKRHGC	3	35	f	f	0	0	3	f	\N	323027
208	Siaya High Court	SYAHGC	SYAHGC	3	40	f	f	0	0	3	f	\N	413056
341	Vihiga High Court	VHGHGC	VHGHGC	3	117	f	f	0	0	3	f	\N	Vihiga High Court
349	Kapsabet High Court	KAPHGC	KAPHGC	3	63	f	f	0	0	3	f	\N	Kapsabet High Court
180	Kericho High Court	KRCHGC	KRCHGC	3	20	f	f	0	0	3	f	\N	353024
346	Kilgoris High Court	KILHGC	KILHGC	3	70	f	f	0	0	3	f	\N	Kilgoris High Court
241	Nyamira Magistrate Court	NYMMGC	NYMMGC	6	38	f	f	0	0	6	f	\N	466101
247	Milimani Commercial Magistrate Court	MILCMC	MILCMC	6	3	f	f	0	0	6	f	\N	476008
250	Nairobi City Court	NRBCTC	NRBCTC	6	2	f	f	0	0	6	f	\N	476061
199	Kapsokwony under Kimilili Magistrate Court	KKWMGC	KKWMGC	6	73	f	f	0	0	6	f	\N	398016
249	Milimani Magistrate Court	MILMGC	MILMGC	6	2	f	f	0	0	6	f	\N	476058
284	Ruiru Magistrate Court	RURMGC	RURMGC	6	139	f	f	0	0	6	f	\N	Ruiru Magistrate Court
296	Msambweni Magistrate Court	MWNMGC	MWNMGC	6	133	f	f	0	0	6	f	\N	Msambweni Magistrate Court
321	Limuru Magistrate Court	LMRMGC	LMRMGC	6	78	f	f	0	0	6	f	\N	226084
324	Dadaab Magistrate Court	DDBMGC	DDBMGC	6	125	f	f	0	0	6	f	\N	Dadaab Magistrate Court
329	Gaitu Mobile Court	GMC	GMC	6	51	f	f	0	0	6	f	\N	Gaitu Mobile Court
299	Wamunyu Mobile Court under Machakos Law Court	WAYMGC	WAYMGC	6	27	f	f	0	0	6	f	\N	Wamunyu Mobile Court under Machakos Law Court
313	Training Law Court	TLC	TLC	6	140	f	f	0	0	6	f	\N	Training Law Court
335	Sololo Mobile Court Under Moyale	SOLMGC	SOLMGC	6	91	f	f	0	0	6	f	\N	Sololo Mobile Court Under Moyale
380	Port Victoria Mobile Court	POVMGC	POVMGC	6	9	f	f	0	0	6	f	\N	Port Victoria Mobile Court
382	Butula Mobile Court	BUTMGC	BUTMGC	6	9	f	f	0	0	6	f	\N	Butula Mobile Court
337	Kipkelion Mobile Court Under Kericho Law Courts	KIPMGC	KIPMGC	6	20	f	f	0	0	6	f	\N	Kipkelion Mobile Court Under Kericho Law Courts
370	Marigat Mobile Court	MARMGC	MARMGC	6	16	f	f	0	0	6	f	\N	Marigat Mobile Court
23	Garsen Magistrate Court	GSNMGC	GSNMGC	6	14	f	f	0	0	6	f	\N	46109
29	Mpeketoni Magistrate Court	MPKMGC	MPKMGC	6	92	f	f	0	0	6	f	\N	56123
187	Sotik Magistrate Court	STKMGC	STKMGC	6	110	f	f	0	0	6	f	\N	366091
191	Butere Magistrate Court	BTRMGC	BTRMGC	6	46	f	f	0	0	6	f	\N	376004
156	Songhor under Kapsabet Magistrate Court	SNGMGC	SNGMGC	6	63	f	f	0	0	6	f	\N	298015
195	Vihiga Magistrate Court	VGHMGC	VGHMGC	6	117	f	f	0	0	6	f	\N	386012
203	Webuye Magistrate Court	WBYMGC	WBYMGC	6	120	f	f	0	0	6	f	\N	396060
211	Ukwala Magistrate Court	UKLMGC	UKLMGC	6	116	f	f	0	0	6	f	\N	416011
219	Nyando Magistrate Court	NYDMGC	NYDMGC	6	101	f	f	0	0	6	f	\N	426102
224	Homabay Magistrate Court	HMBMGC	HMBMGC	6	15	f	f	0	0	6	f	\N	436092
225	Ndhiwa Magistrate Court	NDWMGC	NDWMGC	6	97	f	f	0	0	6	f	\N	436100
231	Migori Magistrate Court	MGRMGC	MGRMGC	6	31	f	f	0	0	6	f	\N	446099
236	Kisii Magistrate Court	KISMGC	KISMGC	6	23	f	f	0	0	6	f	\N	456098
240	Kilgoris Magistrate Court	KLGMGC	KLGMGC	6	70	f	f	0	0	6	f	\N	466097
251	Makadara Magistrate Court	MKDMGC	MKDMGC	6	80	f	f	0	0	6	f	\N	476066
223	Kendu Bay under Oyugis Magistrate Court	KDBMGC	KDBMGC	6	104	f	f	0	0	6	f	\N	438024
351	Merti Magistrate Mobile Court Under Isiolo	MERMGC	MERMGC	6	55	f	f	0	0	6	f	\N	Merti Magistrate Mobile Court Under Isiolo
350	Sereolipi Magistrate Mobile Court Under Isiolo	SERMGC	SERMGC	6	55	f	f	0	0	6	f	\N	Sereolipi Magistrate Mobile Court Under Isiolo
381	Malaba Mobile Court	MALMGC	MALMGC	6	9	f	f	0	0	6	f	\N	Malaba Mobile Court
85	Zombe Mobile Court	ZMBMGC	ZMBMGC	6	25	f	f	0	0	6	f	\N	Zombe Mobile Court
143	Kapenguria Magistrate Court	KPGMGC	KPGMGC	6	19	f	f	0	0	6	f	\N	246053
159	East Pokot under Kabarnet Magistrate Court	EPKMGC	EPKMGC	6	16	f	f	0	0	6	f	\N	308023
6	Mombasa Magistrate Court	MSAMGC	MSAMGC	6	32	f	f	0	0	6	f	\N	16069
8	Tononoka Magistrate Court	TNKMGC	TNKMGC	6	115	f	f	0	0	6	f	\N	16072
17	Kilifi Magistrate Court	KLFMGC	KLFMGC	6	71	f	f	0	0	6	f	\N	36064
24	Hola Magistrate Court	HLAMGC	HLAMGC	6	54	f	f	0	0	6	f	\N	46110
28	Lamu Magistrate Court	LMUMGC	LMUMGC	6	77	f	f	0	0	6	f	\N	56114
290	Bungoma ELRC	BNGERC	BNGERC	4	8	f	f	0	0	4	f	\N	394033
291	Malindi ELRC	MLDERC	MLDERC	4	5	f	f	0	0	4	f	\N	34029
285	Meru Employment and Labour Relations Court	MRUERC	MRUERC	4	30	f	f	0	0	4	f	\N	124031
352	Garissa ELRC	GRSELRC	GRSELRC	4	13	f	f	0	0	4	f	\N	74032
354	Kitale ELRC	KTLERC	KTLERC	4	24	f	f	0	0	4	f	\N	264036
333	Machakos ELRC	MKSERC	MKSERC	4	27	f	f	0	0	4	f	\N	164030
242	Supreme Court	NRBSPC	NRBSPC	1	1	f	f	0	0	3	f	\N	471001
212	Kisumu Court of Appeal	KSMCOA	KSMCOA	2	4	f	f	0	0	2	f	\N	422001
99	Makueni High Court	MKNHGC	MKNHGC	3	28	f	f	0	0	3	f	\N	173060
107	Nyeri High Court	NYRHGC	NYRHGC	3	6	f	f	0	0	3	f	\N	193008
115	Kerugoya High Court	KRGHGC	KRGHGC	3	21	f	f	0	0	3	f	\N	203012
122	Muranga High Court	MRGHGC	MRGHGC	3	33	f	f	0	0	3	f	\N	213007
128	Kiambu High Court	KMBHGC	KMBHGC	3	22	f	f	0	0	3	f	\N	223005
146	Kitale High Court	KTLHGC	KTLHGC	3	24	f	f	0	0	3	f	\N	263018
151	Eldoret High Court	ELDHGC	ELDHGC	3	11	f	f	0	0	3	f	\N	273016
142	Kapenguria High Court	KPGHGC	KPGHGC	3	19	f	f	0	0	3	f	\N	243046
164	Naivasha High Court	NSHHGC	NSHHGC	3	34	f	f	0	0	3	f	\N	323026
173	Narok High Court	NRKHGC	NRKHGC	3	37	f	f	0	0	3	f	\N	333061
213	Kisumu High Court	KSMHGC	KSMHGC	3	4	f	f	0	0	3	f	\N	423004
222	Homabay High Court	HMBHGC	HMBHGC	3	15	f	f	0	0	3	f	\N	433030
108	Nyeri ELRC	NYRERC	NYRERC	4	6	f	f	0	0	4	f	\N	194009
214	Kisumu ELRC	KSMERC	KSMERC	4	4	f	f	0	0	4	f	\N	424005
2	Mombasa ELRC	MSAERC	MSAERC	4	32	f	f	0	0	4	f	\N	14022
33	Voi Magistrate Court	VOIMGC	VOIMGC	6	41	f	f	0	0	6	f	\N	66073
46	Wajir Magistrate Court	WJRMGC	WJRMGC	6	118	f	f	0	0	6	f	\N	86119
51	Mandera Magistrate Court	MNDMGC	MNDMGC	6	82	f	f	0	0	6	f	\N	96115
70	Meru Magistrate Court	MRUMGC	MRUMGC	6	30	f	f	0	0	6	f	\N	126041
77	Marimanti Magistrate Court	MRTMGC	MRTMGC	6	85	f	f	0	0	6	f	\N	136040
81	Embu Magistrate Court	EMBMGC	EMBMGC	6	12	f	f	0	0	6	f	\N	146034
89	Mwingi Magistrate Court	MWGMGC	MWGMGC	6	96	f	f	0	0	6	f	\N	156117
97	Kithimani Magistrate Court	KTMMGC	KTMMGC	6	74	f	f	0	0	6	f	\N	166111
105	Engineer Magistrate Court	ENGMGC	ENGMGC	6	48	f	f	0	0	6	f	\N	186077
113	Othaya Magistrate Court	OTYMGC	OTYMGC	6	103	f	f	0	0	6	f	\N	196029
118	Baricho Magistrate Court	BRCMGC	BRCMGC	6	43	f	f	0	0	6	f	\N	206014
121	Wanguru Magistrate Court	WNGMGC	WNGMGC	6	119	f	f	0	0	6	f	\N	206047
125	Kigumo Magistrate Court	KGMMGC	KGMMGC	6	68	f	f	0	0	6	f	\N	216020
117	Karaba under Wanguru Magistrate Court	KRBMGC	KRBMGC	6	119	f	f	0	0	6	f	\N	208012
130	Kikuyu Magistrate Court	KYKMGC	KYKMGC	6	69	f	f	0	0	6	f	\N	226083
27	Faza Islands under Lamu Magistrate Court	FZIMGC	FZIMGC	6	128	f	f	0	0	6	f	\N	58027
319	Olokurto Mobile Court	OLOKMGC	OLOKMGC	6	37	f	f	0	0	6	f	\N	Olokurto Mobile Court
168	Eldama Ravine Magistrate Court	ERVMGC	ERVMGC	6	47	f	f	0	0	6	f	\N	326076
176	Ngong Magistrate Court	NGNMGC	NGNMGC	6	98	f	f	0	0	6	f	\N	346021
183	Kericho Magistrate Court	KRCMGC	KRCMGC	6	20	f	f	0	0	6	f	\N	356080
\.


--
-- Data for Name: statistics_unitdivision; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_unitdivision (id, division_id, unit_id) FROM stdin;
\.


--
-- Data for Name: statistics_unitrank; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.statistics_unitrank (id, name, is_court) FROM stdin;
10	Committee	f
11	Library	f
12	Directorate	f
13	Other Office	f
14	Small Claim	f
1	Supreme Court	f
2	Court of Appeal	f
3	High Court	f
4	EMPLOYMENT AND LABOUR RELATIONS COURT	t
5	Environment and Land Court	f
6	Magistrate Court	f
7	Kadhi Court	f
8	Tribunal	f
\.


--
-- Data for Name: tasks_comment; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.tasks_comment (id, content, created_at, updated_at, author_id, task_id) FROM stdin;
\.


--
-- Data for Name: tasks_project; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.tasks_project (id, name, description, created_at, updated_at, owner_id, department_id) FROM stdin;
1	ddd	ddd	2025-05-19 13:37:49.801951+00	2025-05-19 13:37:49.801967+00	1	1
2	Computer application I (Theory)		2025-05-20 13:41:07.111604+00	2025-05-20 13:41:07.111621+00	1	4
3	vv	vvv	2025-05-21 11:29:38.356047+00	2025-05-21 11:29:38.356065+00	1	4
\.


--
-- Data for Name: tasks_task; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.tasks_task (id, title, description, status, priority, due_date, created_at, updated_at, creator_id, project_id, start_date, parent_task_id, content_type_id, object_id) FROM stdin;
3	rrr	ggggg	TODO	2	2025-05-28	2025-05-21 12:56:54.021584+00	2025-05-21 12:56:54.021598+00	1	2	\N	\N	\N	\N
4	ff	dddd	TODO	2	2025-05-29	2025-05-21 13:03:00.2097+00	2025-05-21 13:03:00.209715+00	1	2	\N	\N	\N	\N
5	fffffff	ddd	TODO	2	2025-05-29	2025-05-21 13:03:46.933613+00	2025-05-21 13:03:46.933626+00	1	2	\N	\N	\N	\N
6	fffffff	ccc	TODO	2	2025-05-28	2025-05-21 13:07:26.865921+00	2025-05-21 13:07:26.865935+00	1	2	\N	\N	\N	\N
7	qqqqqqqqqqqqq	qq	TODO	2	2025-05-28	2025-05-21 13:08:54.335986+00	2025-05-21 13:08:54.336015+00	1	2	\N	\N	\N	\N
8	qqqqqqqqqqqqq	qqqq	TODO	2	2025-05-26	2025-05-21 13:10:57.493635+00	2025-05-21 13:10:57.493649+00	1	2	\N	\N	\N	\N
9	Lead Security Facilitator	Esse tenetur pariatur minus delectus doloremque officia quo non odio. Ad ad reiciendis perferendis. Dolorem minima doloribus amet pariatur.	TODO	2	2024-09-22	2025-05-21 13:16:44.165195+00	2025-05-21 13:16:44.165208+00	1	1	\N	\N	\N	\N
10	Corporate Infrastructure Associate	Non voluptatem quibusdam laboriosam inventore impedit molestiae enim eos. Eum quas maxime veritatis omnis cumque. Dolorum vero aspernatur iure at magni tempora accusantium est ipsam.	TODO	2	2025-05-23	2025-05-21 13:17:59.942139+00	2025-05-21 13:17:59.942154+00	1	1	\N	\N	\N	\N
11	National Research Officer	Id possimus optio tenetur tenetur vitae beatae aspernatur. Vitae eum maxime voluptas consequuntur minus tempora. Deserunt odit libero tenetur.	TODO	2	2025-06-12	2025-05-21 13:19:37.877303+00	2025-05-21 13:19:37.877318+00	1	3	\N	\N	\N	\N
44	National Assurance Supervisor	Adipisci minus nobis sint laborum repellendus soluta nostrum odio perferendis. Tenetur alias repellendus ea quaerat. Reprehenderit animi incidunt sint illum deleniti nihil quo.	TODO	2	2025-01-15	2025-05-21 13:21:12.449527+00	2025-05-21 13:21:12.449542+00	1	2	\N	\N	\N	\N
45	Investor Directives Manager	Placeat libero laborum reiciendis. Facilis perferendis magni reiciendis id. Commodi cupiditate deleniti sint doloremque blanditiis in temporibus.	TODO	2	2024-12-22	2025-05-21 13:40:02.120159+00	2025-05-21 13:40:02.120179+00	1	1	\N	\N	\N	\N
46	dddddd	ddddd	TODO	2	2025-06-03	2025-05-29 09:21:04.373278+00	2025-05-29 09:21:04.373293+00	1	1	\N	\N	\N	\N
47	Central Directives Developer	Alias nulla adipisci repellat laudantium quidem eaque assumenda cum vitae. Dolorum ut cumque consequuntur necessitatibus accusantium. Molestiae repudiandae minima sint iusto dignissimos voluptatibus.	TODO	2	2025-10-26	2025-05-29 09:21:28.988884+00	2025-05-29 09:21:28.988898+00	1	2	\N	\N	\N	\N
49	Senior Paradigm Executive	Hic error assumenda. Sapiente facilis at quis. Quod perspiciatis velit sint delectus.	TODO	2	2025-07-06	2025-05-29 09:30:04.662853+00	2025-05-29 09:30:04.66287+00	1	3	\N	\N	\N	\N
50	Regional Usability Manager	Id dolor natus necessitatibus magnam voluptate velit itaque cum quas. Ex nobis sapiente quis ex quod sint vero. Ea enim quaerat officia labore inventore officiis quia cum.	TODO	2	2024-10-03	2025-05-29 09:35:24.343985+00	2025-05-29 09:35:24.344+00	1	3	\N	\N	\N	\N
51	Chief Program Consultant	Animi itaque nobis qui fuga laudantium repellat. Nobis amet dolorem sequi quaerat. Reiciendis laboriosam nobis pariatur.	TODO	2	2025-05-29	2025-05-29 09:37:06.76794+00	2025-05-29 09:37:06.767955+00	1	2	\N	\N	\N	\N
52	Senior Identity Designer	Dolor natus recusandae soluta inventore possimus. Possimus iusto eos excepturi quidem cupiditate rerum eos laboriosam neque. Libero facere id pariatur labore facilis corrupti amet facere.	TODO	2	2025-02-03	2025-05-29 09:39:46.396673+00	2025-05-29 09:39:46.396688+00	1	2	\N	\N	\N	\N
53	International Brand Supervisor	Ea exercitationem molestias consequatur magnam consequuntur dolorum quia vero fugiat. Et aperiam saepe harum asperiores eos nobis suscipit. Nostrum tempora aliquam necessitatibus minus iure assumenda.	TODO	2	2025-05-30	2025-05-29 10:53:07.225665+00	2025-05-29 10:53:07.225678+00	1	3	\N	\N	\N	\N
54	Senior Tactics Manager	Laudantium enim totam mollitia porro. Sed debitis id. Excepturi nobis asperiores tempore soluta cupiditate.	TODO	2	2024-08-23	2025-05-29 10:56:22.713835+00	2025-05-29 10:56:22.71385+00	1	2	\N	\N	\N	\N
61	Dynamic Applications Producer	Iste dolor nihil deleniti minima reprehenderit pariatur ducimus quae illum. Odio tempora adipisci doloremque. Praesentium laboriosam dolorem minus iste numquam.	TODO	2	2025-07-07	2025-07-02 11:01:10.294934+00	2025-07-02 11:01:10.294948+00	1	2	\N	\N	\N	\N
56	Corporate Mobility Orchestrator	Corporis illum dolorum. Eum assumenda neque beatae cupiditate autem reiciendis repellat. Beatae labore odit debitis praesentium.	IN_REVIEW	2	2025-06-27	2025-05-29 11:38:21.275849+00	2025-05-29 11:39:18.098889+00	1	3	\N	\N	\N	\N
57	Ngobiro	Ngobiro	TODO	2	2025-06-05	2025-05-29 11:45:38.631887+00	2025-05-29 11:45:38.631903+00	1	1	\N	\N	\N	\N
62	Customer Identity Associate	Odit eaque commodi nostrum minus amet facilis. Laudantium rerum dolores. Blanditiis ab ipsa maxime tenetur architecto beatae nam nulla.	TODO	2	2025-07-06	2025-07-02 12:03:35.636791+00	2025-07-02 12:03:35.636804+00	1	1	\N	\N	\N	\N
59	Dynamic Response Coordinator	Nobis nemo laboriosam nam fuga corporis id. Maxime voluptatem quam occaecati minus expedita reprehenderit earum at. Repellendus sapiente non alias eaque voluptates veritatis possimus quaerat.	DONE	2	2024-12-20	2025-06-09 09:27:04.379492+00	2025-06-30 12:12:29.064535+00	21	2	\N	\N	\N	\N
48	Investor Tactics Agent	Porro harum delectus iure voluptatum occaecati similique recusandae modi sunt. Corrupti iste nemo. Rerum consequatur nulla quasi.	DONE	2	2026-03-07	2025-05-29 09:24:15.72854+00	2025-05-29 11:32:34.887351+00	1	3	\N	\N	\N	\N
58	Principal Infrastructure Supervisor	Odit aliquam repellat alias officiis nisi voluptas neque quas. Incidunt illum voluptates cupiditate aliquam accusamus sed illum blanditiis. Quibusdam enim non illum blanditiis nemo quidem.	DONE	2	2025-11-05	2025-06-03 14:30:50.920499+00	2025-07-02 10:55:14.956059+00	21	3	\N	\N	\N	\N
55	Lead Paradigm Director	Eveniet amet est molestiae maiores accusantium atque quos porro accusantium. Iste excepturi quisquam hic quibusdam iste. Dignissimos aliquid officia nulla fugiat voluptate eaque facere magnam minima.	IN_PROGRESS	2	2025-10-09	2025-05-29 10:58:04.636444+00	2025-05-29 11:33:40.216984+00	1	3	\N	\N	\N	\N
60	Dynamic Infrastructure Consultant	Rem facilis ex nihil nobis sapiente. Pariatur quidem aperiam sequi. Laboriosam pariatur ea ad nesciunt nesciunt reprehenderit reiciendis omnis labore.	TODO	2	2025-07-23	2025-07-02 10:59:43.741772+00	2025-07-02 10:59:43.741785+00	1	3	\N	\N	\N	\N
\.


--
-- Data for Name: tasks_task_assignees; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.tasks_task_assignees (id, task_id, customuser_id) FROM stdin;
1	45	20
2	45	3
3	45	4
4	45	10
5	45	11
6	45	12
7	45	16
8	46	13
9	46	15
10	46	16
11	47	5
12	47	10
13	47	11
14	47	12
15	47	18
16	47	19
23	49	3
24	49	8
25	49	10
26	49	12
27	49	18
28	50	2
29	50	4
30	50	5
31	50	6
32	50	7
33	50	8
34	50	9
35	50	14
36	50	15
37	50	17
38	50	18
39	50	19
40	51	20
41	51	3
42	51	6
43	51	7
44	51	10
45	51	11
46	51	12
47	51	18
48	51	19
49	52	2
50	52	3
51	52	6
52	52	8
53	52	10
54	52	17
55	52	19
56	53	20
57	54	19
58	55	5
65	48	20
66	48	4
67	48	6
68	48	13
69	48	16
70	48	19
71	56	2
72	57	21
82	59	21
83	58	21
\.


--
-- Data for Name: tasks_taskhistory; Type: TABLE DATA; Schema: public; Owner: dspop_user
--

COPY public.tasks_taskhistory (id, "timestamp", comment, task_id, user_id, task_state, change_description) FROM stdin;
1	2025-05-29 11:25:24.104226+00	\N	48	1	{}	
2	2025-05-29 11:28:58.977429+00	Status changed from Approved to In Progress	48	1	{"title": "Investor Tactics Agent", "status": "IN_PROGRESS", "due_date": "2026-03-07", "priority": 2, "assignees": [20, 4, 6, 13, 16, 19], "description": "Porro harum delectus iure voluptatum occaecati similique recusandae modi sunt. Corrupti iste nemo. Rerum consequatur nulla quasi."}	
3	2025-05-29 11:29:12.262721+00	Status changed from In Progress to Reassigned	48	1	{"title": "Investor Tactics Agent", "status": "REASSIGNED", "due_date": "2026-03-07", "priority": 2, "assignees": [20, 4, 6, 13, 16, 19], "description": "Porro harum delectus iure voluptatum occaecati similique recusandae modi sunt. Corrupti iste nemo. Rerum consequatur nulla quasi."}	
4	2025-05-29 11:29:24.017756+00	Status changed from Reassigned to Blocked	48	1	{"title": "Investor Tactics Agent", "status": "BLOCKED", "due_date": "2026-03-07", "priority": 2, "assignees": [20, 4, 6, 13, 16, 19], "description": "Porro harum delectus iure voluptatum occaecati similique recusandae modi sunt. Corrupti iste nemo. Rerum consequatur nulla quasi."}	
5	2025-05-29 11:29:51.950369+00	Status changed from Blocked to Done	48	1	{"title": "Investor Tactics Agent", "status": "DONE", "due_date": "2026-03-07", "priority": 2, "assignees": [20, 4, 6, 13, 16, 19], "description": "Porro harum delectus iure voluptatum occaecati similique recusandae modi sunt. Corrupti iste nemo. Rerum consequatur nulla quasi."}	
6	2025-05-29 11:33:29.446513+00	Status changed from To Do to To Do	55	1	{"title": "Lead Paradigm Director", "status": "TODO", "due_date": "2025-10-09", "priority": 2, "assignees": [5], "description": "Eveniet amet est molestiae maiores accusantium atque quos porro accusantium. Iste excepturi quisquam hic quibusdam iste. Dignissimos aliquid officia nulla fugiat voluptate eaque facere magnam minima."}	
7	2025-05-29 11:33:40.239304+00	Status changed from To Do to In Progress	55	1	{"title": "Lead Paradigm Director", "status": "IN_PROGRESS", "due_date": "2025-10-09", "priority": 2, "assignees": [5], "description": "Eveniet amet est molestiae maiores accusantium atque quos porro accusantium. Iste excepturi quisquam hic quibusdam iste. Dignissimos aliquid officia nulla fugiat voluptate eaque facere magnam minima."}	
8	2025-05-29 11:39:04.279533+00	Status changed from To Do to In Progress	56	1	{"title": "Corporate Mobility Orchestrator", "status": "IN_PROGRESS", "due_date": "2025-06-27", "priority": 2, "assignees": [2], "description": "Corporis illum dolorum. Eum assumenda neque beatae cupiditate autem reiciendis repellat. Beatae labore odit debitis praesentium."}	
9	2025-05-29 11:39:18.112848+00	Status changed from In Progress to In Review	56	1	{"title": "Corporate Mobility Orchestrator", "status": "IN_REVIEW", "due_date": "2025-06-27", "priority": 2, "assignees": [2], "description": "Corporis illum dolorum. Eum assumenda neque beatae cupiditate autem reiciendis repellat. Beatae labore odit debitis praesentium."}	
10	2025-06-09 11:47:18.828919+00	Status changed from To Do to Approved	58	21	{"title": "Principal Infrastructure Supervisor", "status": "APPROVED", "due_date": "2025-11-05", "priority": 2, "assignees": [2, 3, 6, 8, 10, 11, 12, 16, 1], "description": "Odit aliquam repellat alias officiis nisi voluptas neque quas. Incidunt illum voluptates cupiditate aliquam accusamus sed illum blanditiis. Quibusdam enim non illum blanditiis nemo quidem."}	
11	2025-06-30 12:12:29.09196+00	Status changed from To Do to Done	59	21	{"title": "Dynamic Response Coordinator", "status": "DONE", "due_date": "2024-12-20", "priority": 2, "assignees": [21], "description": "Nobis nemo laboriosam nam fuga corporis id. Maxime voluptatem quam occaecati minus expedita reprehenderit earum at. Repellendus sapiente non alias eaque voluptates veritatis possimus quaerat."}	
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 255, true);


--
-- Name: authentication_customuser_departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.authentication_customuser_departments_id_seq', 32, true);


--
-- Name: authentication_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.authentication_customuser_groups_id_seq', 1, false);


--
-- Name: authentication_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.authentication_customuser_id_seq', 21, true);


--
-- Name: authentication_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.authentication_customuser_user_permissions_id_seq', 1, false);


--
-- Name: budget_budgetcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.budget_budgetcategory_id_seq', 1, false);


--
-- Name: budget_financialyear_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.budget_financialyear_id_seq', 1, false);


--
-- Name: budget_performanceindicator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.budget_performanceindicator_id_seq', 1, false);


--
-- Name: budget_quarterlyallocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.budget_quarterlyallocation_id_seq', 1, false);


--
-- Name: budget_transformativeinitiative_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.budget_transformativeinitiative_id_seq', 1, false);


--
-- Name: budget_workplanitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.budget_workplanitem_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 2, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 60, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 73, true);


--
-- Name: document_management_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.document_management_document_id_seq', 41, true);


--
-- Name: document_management_documentaccess_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.document_management_documentaccess_id_seq', 15, true);


--
-- Name: document_management_documentactivity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.document_management_documentactivity_id_seq', 15, true);


--
-- Name: document_management_documentcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.document_management_documentcategory_id_seq', 1, false);


--
-- Name: document_management_documentcomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.document_management_documentcomment_id_seq', 5, true);


--
-- Name: home_module_departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.home_module_departments_id_seq', 2, true);


--
-- Name: home_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.home_module_id_seq', 12, true);


--
-- Name: innovations_innovation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.innovations_innovation_id_seq', 1, false);


--
-- Name: innovations_innovationattachment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.innovations_innovationattachment_id_seq', 1, false);


--
-- Name: mail_mailactivity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.mail_mailactivity_id_seq', 1, false);


--
-- Name: mail_mailassignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.mail_mailassignment_id_seq', 1, false);


--
-- Name: mail_mailattachment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.mail_mailattachment_id_seq', 1, false);


--
-- Name: mail_mailmovement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.mail_mailmovement_id_seq', 1, false);


--
-- Name: mail_physicalmail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.mail_physicalmail_id_seq', 1, false);


--
-- Name: meetings_meeting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.meetings_meeting_id_seq', 187, true);


--
-- Name: meetings_meetingaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.meetings_meetingaction_id_seq', 1, false);


--
-- Name: meetings_meetingdocument_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.meetings_meetingdocument_id_seq', 1, false);


--
-- Name: meetings_meetingparticipant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.meetings_meetingparticipant_id_seq', 59, true);


--
-- Name: meetings_meetingtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.meetings_meetingtype_id_seq', 8, true);


--
-- Name: memos_memo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memo_id_seq', 1, false);


--
-- Name: memos_memo_recipient_departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memo_recipient_departments_id_seq', 1, false);


--
-- Name: memos_memo_recipient_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memo_recipient_users_id_seq', 1, false);


--
-- Name: memos_memoactivity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memoactivity_id_seq', 1, false);


--
-- Name: memos_memoapproval_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memoapproval_id_seq', 1, false);


--
-- Name: memos_memocomment_attachments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memocomment_attachments_id_seq', 1, false);


--
-- Name: memos_memocomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memocomment_id_seq', 1, false);


--
-- Name: memos_memotemplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memotemplate_id_seq', 1, false);


--
-- Name: memos_memoversion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.memos_memoversion_id_seq', 1, false);


--
-- Name: organization_department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.organization_department_id_seq', 5, true);


--
-- Name: organization_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.organization_role_id_seq', 5, true);


--
-- Name: organization_role_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.organization_role_permissions_id_seq', 1, false);


--
-- Name: organization_userrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.organization_userrole_id_seq', 20, true);


--
-- Name: pmmu_financialyearperformance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.pmmu_financialyearperformance_id_seq', 1, false);


--
-- Name: pmmu_indicatorcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.pmmu_indicatorcategory_id_seq', 1, false);


--
-- Name: pmmu_indicatornote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.pmmu_indicatornote_id_seq', 55, true);


--
-- Name: pmmu_performanceindicator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.pmmu_performanceindicator_id_seq', 17, true);


--
-- Name: pmmu_pmmu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.pmmu_pmmu_id_seq', 2, true);


--
-- Name: statistics_adjournmentreason_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_adjournmentreason_id_seq', 21, true);


--
-- Name: statistics_caseactivitytype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_caseactivitytype_id_seq', 1, false);


--
-- Name: statistics_casecategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_casecategory_id_seq', 6, true);


--
-- Name: statistics_caseoutcome_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_caseoutcome_id_seq', 1, false);


--
-- Name: statistics_dcrtdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_dcrtdata_id_seq', 1, false);


--
-- Name: statistics_division_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_division_id_seq', 96, true);


--
-- Name: statistics_financialquarter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_financialquarter_id_seq', 4, true);


--
-- Name: statistics_financialyear_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_financialyear_id_seq', 1, true);


--
-- Name: statistics_months_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_months_id_seq', 12, true);


--
-- Name: statistics_unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_unit_id_seq', 1, false);


--
-- Name: statistics_unitdivision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_unitdivision_id_seq', 1, false);


--
-- Name: statistics_unitrank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.statistics_unitrank_id_seq', 14, true);


--
-- Name: tasks_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.tasks_comment_id_seq', 1, false);


--
-- Name: tasks_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.tasks_project_id_seq', 3, true);


--
-- Name: tasks_task_assignees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.tasks_task_assignees_id_seq', 83, true);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.tasks_task_id_seq', 62, true);


--
-- Name: tasks_taskhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dspop_user
--

SELECT pg_catalog.setval('public.tasks_taskhistory_id_seq', 11, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authentication_customuser_departments authentication_customuse_customuser_id_department_fad3ca10_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_departments
    ADD CONSTRAINT authentication_customuse_customuser_id_department_fad3ca10_uniq UNIQUE (customuser_id, department_id);


--
-- Name: authentication_customuser_groups authentication_customuse_customuser_id_group_id_8a637646_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_groups
    ADD CONSTRAINT authentication_customuse_customuser_id_group_id_8a637646_uniq UNIQUE (customuser_id, group_id);


--
-- Name: authentication_customuser_user_permissions authentication_customuse_customuser_id_permission_923704b1_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_user_permissions
    ADD CONSTRAINT authentication_customuse_customuser_id_permission_923704b1_uniq UNIQUE (customuser_id, permission_id);


--
-- Name: authentication_customuser_departments authentication_customuser_departments_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_departments
    ADD CONSTRAINT authentication_customuser_departments_pkey PRIMARY KEY (id);


--
-- Name: authentication_customuser_groups authentication_customuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_groups
    ADD CONSTRAINT authentication_customuser_groups_pkey PRIMARY KEY (id);


--
-- Name: authentication_customuser authentication_customuser_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser
    ADD CONSTRAINT authentication_customuser_pkey PRIMARY KEY (id);


--
-- Name: authentication_customuser_user_permissions authentication_customuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_user_permissions
    ADD CONSTRAINT authentication_customuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: authentication_customuser authentication_customuser_username_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser
    ADD CONSTRAINT authentication_customuser_username_key UNIQUE (username);


--
-- Name: budget_budgetcategory budget_budgetcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_budgetcategory
    ADD CONSTRAINT budget_budgetcategory_pkey PRIMARY KEY (id);


--
-- Name: budget_financialyear budget_financialyear_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_financialyear
    ADD CONSTRAINT budget_financialyear_pkey PRIMARY KEY (id);


--
-- Name: budget_performanceindicator budget_performanceindicator_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_performanceindicator
    ADD CONSTRAINT budget_performanceindicator_pkey PRIMARY KEY (id);


--
-- Name: budget_quarterlyallocation budget_quarterlyallocati_workplan_item_id_quarter_5ddbf11b_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_quarterlyallocation
    ADD CONSTRAINT budget_quarterlyallocati_workplan_item_id_quarter_5ddbf11b_uniq UNIQUE (workplan_item_id, quarter);


--
-- Name: budget_quarterlyallocation budget_quarterlyallocation_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_quarterlyallocation
    ADD CONSTRAINT budget_quarterlyallocation_pkey PRIMARY KEY (id);


--
-- Name: budget_transformativeinitiative budget_transformativeinitiative_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_transformativeinitiative
    ADD CONSTRAINT budget_transformativeinitiative_pkey PRIMARY KEY (id);


--
-- Name: budget_transformativeinitiative budget_transformativeinitiative_workplan_item_id_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_transformativeinitiative
    ADD CONSTRAINT budget_transformativeinitiative_workplan_item_id_key UNIQUE (workplan_item_id);


--
-- Name: budget_workplanitem budget_workplanitem_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_workplanitem
    ADD CONSTRAINT budget_workplanitem_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: document_management_documentaccess document_management_docu_document_id_user_id_592cdbd8_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentaccess
    ADD CONSTRAINT document_management_docu_document_id_user_id_592cdbd8_uniq UNIQUE (document_id, user_id);


--
-- Name: document_management_document document_management_document_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_document
    ADD CONSTRAINT document_management_document_pkey PRIMARY KEY (id);


--
-- Name: document_management_documentaccess document_management_documentaccess_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentaccess
    ADD CONSTRAINT document_management_documentaccess_pkey PRIMARY KEY (id);


--
-- Name: document_management_documentactivity document_management_documentactivity_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentactivity
    ADD CONSTRAINT document_management_documentactivity_pkey PRIMARY KEY (id);


--
-- Name: document_management_documentcategory document_management_documentcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcategory
    ADD CONSTRAINT document_management_documentcategory_pkey PRIMARY KEY (id);


--
-- Name: document_management_documentcomment document_management_documentcomment_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcomment
    ADD CONSTRAINT document_management_documentcomment_pkey PRIMARY KEY (id);


--
-- Name: home_module_departments home_module_departments_module_id_department_id_f8443bc9_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module_departments
    ADD CONSTRAINT home_module_departments_module_id_department_id_f8443bc9_uniq UNIQUE (module_id, department_id);


--
-- Name: home_module_departments home_module_departments_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module_departments
    ADD CONSTRAINT home_module_departments_pkey PRIMARY KEY (id);


--
-- Name: home_module home_module_name_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module
    ADD CONSTRAINT home_module_name_key UNIQUE (name);


--
-- Name: home_module home_module_permission_codename_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module
    ADD CONSTRAINT home_module_permission_codename_key UNIQUE (permission_codename);


--
-- Name: home_module home_module_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module
    ADD CONSTRAINT home_module_pkey PRIMARY KEY (id);


--
-- Name: innovations_innovation innovations_innovation_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovation
    ADD CONSTRAINT innovations_innovation_pkey PRIMARY KEY (id);


--
-- Name: innovations_innovationattachment innovations_innovationattachment_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovationattachment
    ADD CONSTRAINT innovations_innovationattachment_pkey PRIMARY KEY (id);


--
-- Name: mail_mailactivity mail_mailactivity_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailactivity
    ADD CONSTRAINT mail_mailactivity_pkey PRIMARY KEY (id);


--
-- Name: mail_mailassignment mail_mailassignment_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailassignment
    ADD CONSTRAINT mail_mailassignment_pkey PRIMARY KEY (id);


--
-- Name: mail_mailattachment mail_mailattachment_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailattachment
    ADD CONSTRAINT mail_mailattachment_pkey PRIMARY KEY (id);


--
-- Name: mail_mailmovement mail_mailmovement_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailmovement
    ADD CONSTRAINT mail_mailmovement_pkey PRIMARY KEY (id);


--
-- Name: mail_physicalmail mail_physicalmail_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_physicalmail
    ADD CONSTRAINT mail_physicalmail_pkey PRIMARY KEY (id);


--
-- Name: mail_physicalmail mail_physicalmail_tracking_number_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_physicalmail
    ADD CONSTRAINT mail_physicalmail_tracking_number_key UNIQUE (tracking_number);


--
-- Name: meetings_meeting meetings_meeting_date_title_organizer_id_647d76fe_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting
    ADD CONSTRAINT meetings_meeting_date_title_organizer_id_647d76fe_uniq UNIQUE (date, title, organizer_id);


--
-- Name: meetings_meeting meetings_meeting_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting
    ADD CONSTRAINT meetings_meeting_pkey PRIMARY KEY (id);


--
-- Name: meetings_meetingaction meetings_meetingaction_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingaction
    ADD CONSTRAINT meetings_meetingaction_pkey PRIMARY KEY (id);


--
-- Name: meetings_meetingdocument meetings_meetingdocument_meeting_id_document_id_b6e2d6d9_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingdocument
    ADD CONSTRAINT meetings_meetingdocument_meeting_id_document_id_b6e2d6d9_uniq UNIQUE (meeting_id, document_id);


--
-- Name: meetings_meetingdocument meetings_meetingdocument_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingdocument
    ADD CONSTRAINT meetings_meetingdocument_pkey PRIMARY KEY (id);


--
-- Name: meetings_meetingparticipant meetings_meetingparticip_meeting_id_participant_i_b72ad90b_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingparticipant
    ADD CONSTRAINT meetings_meetingparticip_meeting_id_participant_i_b72ad90b_uniq UNIQUE (meeting_id, participant_id);


--
-- Name: meetings_meetingparticipant meetings_meetingparticipant_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingparticipant
    ADD CONSTRAINT meetings_meetingparticipant_pkey PRIMARY KEY (id);


--
-- Name: meetings_meetingtype meetings_meetingtype_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingtype
    ADD CONSTRAINT meetings_meetingtype_pkey PRIMARY KEY (id);


--
-- Name: memos_memo memos_memo_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_pkey PRIMARY KEY (id);


--
-- Name: memos_memo_recipient_departments memos_memo_recipient_dep_memo_id_department_id_c529a901_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_departments
    ADD CONSTRAINT memos_memo_recipient_dep_memo_id_department_id_c529a901_uniq UNIQUE (memo_id, department_id);


--
-- Name: memos_memo_recipient_departments memos_memo_recipient_departments_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_departments
    ADD CONSTRAINT memos_memo_recipient_departments_pkey PRIMARY KEY (id);


--
-- Name: memos_memo_recipient_users memos_memo_recipient_users_memo_id_customuser_id_f68e6b8a_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_users
    ADD CONSTRAINT memos_memo_recipient_users_memo_id_customuser_id_f68e6b8a_uniq UNIQUE (memo_id, customuser_id);


--
-- Name: memos_memo_recipient_users memos_memo_recipient_users_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_users
    ADD CONSTRAINT memos_memo_recipient_users_pkey PRIMARY KEY (id);


--
-- Name: memos_memo memos_memo_reference_number_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_reference_number_key UNIQUE (reference_number);


--
-- Name: memos_memoactivity memos_memoactivity_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoactivity
    ADD CONSTRAINT memos_memoactivity_pkey PRIMARY KEY (id);


--
-- Name: memos_memoapproval memos_memoapproval_memo_id_approver_id_level_70f2532d_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoapproval
    ADD CONSTRAINT memos_memoapproval_memo_id_approver_id_level_70f2532d_uniq UNIQUE (memo_id, approver_id, level);


--
-- Name: memos_memoapproval memos_memoapproval_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoapproval
    ADD CONSTRAINT memos_memoapproval_pkey PRIMARY KEY (id);


--
-- Name: memos_memocomment_attachments memos_memocomment_attach_memocomment_id_document__bfb1bafc_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment_attachments
    ADD CONSTRAINT memos_memocomment_attach_memocomment_id_document__bfb1bafc_uniq UNIQUE (memocomment_id, document_id);


--
-- Name: memos_memocomment_attachments memos_memocomment_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment_attachments
    ADD CONSTRAINT memos_memocomment_attachments_pkey PRIMARY KEY (id);


--
-- Name: memos_memocomment memos_memocomment_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment
    ADD CONSTRAINT memos_memocomment_pkey PRIMARY KEY (id);


--
-- Name: memos_memotemplate memos_memotemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memotemplate
    ADD CONSTRAINT memos_memotemplate_pkey PRIMARY KEY (id);


--
-- Name: memos_memoversion memos_memoversion_memo_id_version_number_b39d28fb_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoversion
    ADD CONSTRAINT memos_memoversion_memo_id_version_number_b39d28fb_uniq UNIQUE (memo_id, version_number);


--
-- Name: memos_memoversion memos_memoversion_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoversion
    ADD CONSTRAINT memos_memoversion_pkey PRIMARY KEY (id);


--
-- Name: organization_department organization_department_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_department
    ADD CONSTRAINT organization_department_pkey PRIMARY KEY (id);


--
-- Name: organization_role_permissions organization_role_permis_role_id_permission_id_0f6548c8_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role_permissions
    ADD CONSTRAINT organization_role_permis_role_id_permission_id_0f6548c8_uniq UNIQUE (role_id, permission_id);


--
-- Name: organization_role_permissions organization_role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role_permissions
    ADD CONSTRAINT organization_role_permissions_pkey PRIMARY KEY (id);


--
-- Name: organization_role organization_role_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role
    ADD CONSTRAINT organization_role_pkey PRIMARY KEY (id);


--
-- Name: organization_userrole organization_userrole_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_userrole
    ADD CONSTRAINT organization_userrole_pkey PRIMARY KEY (id);


--
-- Name: organization_userrole organization_userrole_user_id_role_id_6d7ba8d8_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_userrole
    ADD CONSTRAINT organization_userrole_user_id_role_id_6d7ba8d8_uniq UNIQUE (user_id, role_id);


--
-- Name: pmmu_financialyearperformance pmmu_financialyearperfor_financial_year_id_indica_b8e58944_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_financialyearperformance
    ADD CONSTRAINT pmmu_financialyearperfor_financial_year_id_indica_b8e58944_uniq UNIQUE (financial_year_id, indicator_id);


--
-- Name: pmmu_financialyearperformance pmmu_financialyearperformance_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_financialyearperformance
    ADD CONSTRAINT pmmu_financialyearperformance_pkey PRIMARY KEY (id);


--
-- Name: pmmu_indicatorcategory pmmu_indicatorcategory_name_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatorcategory
    ADD CONSTRAINT pmmu_indicatorcategory_name_key UNIQUE (name);


--
-- Name: pmmu_indicatorcategory pmmu_indicatorcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatorcategory
    ADD CONSTRAINT pmmu_indicatorcategory_pkey PRIMARY KEY (id);


--
-- Name: pmmu_indicatornote pmmu_indicatornote_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatornote
    ADD CONSTRAINT pmmu_indicatornote_pkey PRIMARY KEY (id);


--
-- Name: pmmu_performanceindicator pmmu_performanceindicator_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_performanceindicator
    ADD CONSTRAINT pmmu_performanceindicator_pkey PRIMARY KEY (id);


--
-- Name: pmmu_pmmu pmmu_pmmu_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_pmmu
    ADD CONSTRAINT pmmu_pmmu_pkey PRIMARY KEY (id);


--
-- Name: statistics_adjournmentreason statistics_adjournmentreason_name_unit_rank_id_235ec52e_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_adjournmentreason
    ADD CONSTRAINT statistics_adjournmentreason_name_unit_rank_id_235ec52e_uniq UNIQUE (name, unit_rank_id);


--
-- Name: statistics_adjournmentreason statistics_adjournmentreason_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_adjournmentreason
    ADD CONSTRAINT statistics_adjournmentreason_pkey PRIMARY KEY (id);


--
-- Name: statistics_caseactivitytype statistics_caseactivitytype_name_bcd7025f_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseactivitytype
    ADD CONSTRAINT statistics_caseactivitytype_name_bcd7025f_uniq UNIQUE (name);


--
-- Name: statistics_caseactivitytype statistics_caseactivitytype_name_unit_rank_id_f28941fd_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseactivitytype
    ADD CONSTRAINT statistics_caseactivitytype_name_unit_rank_id_f28941fd_uniq UNIQUE (name, unit_rank_id);


--
-- Name: statistics_caseactivitytype statistics_caseactivitytype_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseactivitytype
    ADD CONSTRAINT statistics_caseactivitytype_pkey PRIMARY KEY (id);


--
-- Name: statistics_casecategory statistics_casecategory_code_unit_rank_id_9abab41b_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_casecategory
    ADD CONSTRAINT statistics_casecategory_code_unit_rank_id_9abab41b_uniq UNIQUE (code, unit_rank_id);


--
-- Name: statistics_casecategory statistics_casecategory_name_unit_rank_id_68c98cb5_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_casecategory
    ADD CONSTRAINT statistics_casecategory_name_unit_rank_id_68c98cb5_uniq UNIQUE (name, unit_rank_id);


--
-- Name: statistics_casecategory statistics_casecategory_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_casecategory
    ADD CONSTRAINT statistics_casecategory_pkey PRIMARY KEY (id);


--
-- Name: statistics_caseoutcome statistics_caseoutcome_name_unit_rank_id_1115d75b_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseoutcome
    ADD CONSTRAINT statistics_caseoutcome_name_unit_rank_id_1115d75b_uniq UNIQUE (name, unit_rank_id);


--
-- Name: statistics_caseoutcome statistics_caseoutcome_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseoutcome
    ADD CONSTRAINT statistics_caseoutcome_pkey PRIMARY KEY (id);


--
-- Name: statistics_dcrtdata statistics_dcrtdata_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_pkey PRIMARY KEY (id);


--
-- Name: statistics_division statistics_division_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_division
    ADD CONSTRAINT statistics_division_pkey PRIMARY KEY (id);


--
-- Name: statistics_financialquarter statistics_financialquarter_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_financialquarter
    ADD CONSTRAINT statistics_financialquarter_pkey PRIMARY KEY (id);


--
-- Name: statistics_financialyear statistics_financialyear_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_financialyear
    ADD CONSTRAINT statistics_financialyear_pkey PRIMARY KEY (id);


--
-- Name: statistics_months statistics_months_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_months
    ADD CONSTRAINT statistics_months_pkey PRIMARY KEY (id);


--
-- Name: statistics_unit statistics_unit_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unit
    ADD CONSTRAINT statistics_unit_pkey PRIMARY KEY (id);


--
-- Name: statistics_unitdivision statistics_unitdivision_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unitdivision
    ADD CONSTRAINT statistics_unitdivision_pkey PRIMARY KEY (id);


--
-- Name: statistics_unitrank statistics_unitrank_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unitrank
    ADD CONSTRAINT statistics_unitrank_pkey PRIMARY KEY (id);


--
-- Name: tasks_comment tasks_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_comment
    ADD CONSTRAINT tasks_comment_pkey PRIMARY KEY (id);


--
-- Name: tasks_project tasks_project_name_key; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_project
    ADD CONSTRAINT tasks_project_name_key UNIQUE (name);


--
-- Name: tasks_project tasks_project_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_project
    ADD CONSTRAINT tasks_project_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_assignees tasks_task_assignees_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task_assignees
    ADD CONSTRAINT tasks_task_assignees_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_assignees tasks_task_assignees_task_id_customuser_id_3e41a718_uniq; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task_assignees
    ADD CONSTRAINT tasks_task_assignees_task_id_customuser_id_3e41a718_uniq UNIQUE (task_id, customuser_id);


--
-- Name: tasks_task tasks_task_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_pkey PRIMARY KEY (id);


--
-- Name: tasks_taskhistory tasks_taskhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_taskhistory
    ADD CONSTRAINT tasks_taskhistory_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authentication_customuser__customuser_id_33d2a5f7; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser__customuser_id_33d2a5f7 ON public.authentication_customuser_user_permissions USING btree (customuser_id);


--
-- Name: authentication_customuser__permission_id_e47332af; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser__permission_id_e47332af ON public.authentication_customuser_user_permissions USING btree (permission_id);


--
-- Name: authentication_customuser_departments_customuser_id_23099396; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser_departments_customuser_id_23099396 ON public.authentication_customuser_departments USING btree (customuser_id);


--
-- Name: authentication_customuser_departments_department_id_a87ebd05; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser_departments_department_id_a87ebd05 ON public.authentication_customuser_departments USING btree (department_id);


--
-- Name: authentication_customuser_groups_customuser_id_a7d1343c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser_groups_customuser_id_a7d1343c ON public.authentication_customuser_groups USING btree (customuser_id);


--
-- Name: authentication_customuser_groups_group_id_c5ef1d10; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser_groups_group_id_c5ef1d10 ON public.authentication_customuser_groups USING btree (group_id);


--
-- Name: authentication_customuser_username_3dffdf84_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX authentication_customuser_username_3dffdf84_like ON public.authentication_customuser USING btree (username varchar_pattern_ops);


--
-- Name: budget_performanceindicator_workplan_item_id_67607840; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX budget_performanceindicator_workplan_item_id_67607840 ON public.budget_performanceindicator USING btree (workplan_item_id);


--
-- Name: budget_quarterlyallocation_workplan_item_id_9abab4fe; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX budget_quarterlyallocation_workplan_item_id_9abab4fe ON public.budget_quarterlyallocation USING btree (workplan_item_id);


--
-- Name: budget_workplanitem_category_id_e1a4fd25; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX budget_workplanitem_category_id_e1a4fd25 ON public.budget_workplanitem USING btree (category_id);


--
-- Name: budget_workplanitem_financial_year_id_01db6d20; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX budget_workplanitem_financial_year_id_01db6d20 ON public.budget_workplanitem USING btree (financial_year_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: document_management_document_category_id_08d18950; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_document_category_id_08d18950 ON public.document_management_document USING btree (category_id);


--
-- Name: document_management_document_content_type_id_bfaa50ba; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_document_content_type_id_bfaa50ba ON public.document_management_document USING btree (content_type_id);


--
-- Name: document_management_document_parent_document_id_083a3a5f; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_document_parent_document_id_083a3a5f ON public.document_management_document USING btree (parent_document_id);


--
-- Name: document_management_document_uploaded_by_id_7769bbfb; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_document_uploaded_by_id_7769bbfb ON public.document_management_document USING btree (uploaded_by_id);


--
-- Name: document_management_documentaccess_document_id_b32bcc6f; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentaccess_document_id_b32bcc6f ON public.document_management_documentaccess USING btree (document_id);


--
-- Name: document_management_documentaccess_granted_by_id_cf38c85d; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentaccess_granted_by_id_cf38c85d ON public.document_management_documentaccess USING btree (granted_by_id);


--
-- Name: document_management_documentaccess_user_id_f1c1064b; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentaccess_user_id_f1c1064b ON public.document_management_documentaccess USING btree (user_id);


--
-- Name: document_management_documentactivity_document_id_460e6b78; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentactivity_document_id_460e6b78 ON public.document_management_documentactivity USING btree (document_id);


--
-- Name: document_management_documentactivity_user_id_547c27be; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentactivity_user_id_547c27be ON public.document_management_documentactivity USING btree (user_id);


--
-- Name: document_management_documentcomment_author_id_1723f1a6; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentcomment_author_id_1723f1a6 ON public.document_management_documentcomment USING btree (author_id);


--
-- Name: document_management_documentcomment_document_id_68309093; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentcomment_document_id_68309093 ON public.document_management_documentcomment USING btree (document_id);


--
-- Name: document_management_documentcomment_parent_comment_id_e9cd7f2c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX document_management_documentcomment_parent_comment_id_e9cd7f2c ON public.document_management_documentcomment USING btree (parent_comment_id);


--
-- Name: home_module_departments_department_id_1495a1bd; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX home_module_departments_department_id_1495a1bd ON public.home_module_departments USING btree (department_id);


--
-- Name: home_module_departments_module_id_f6eb1aa1; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX home_module_departments_module_id_f6eb1aa1 ON public.home_module_departments USING btree (module_id);


--
-- Name: home_module_name_75a62026_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX home_module_name_75a62026_like ON public.home_module USING btree (name varchar_pattern_ops);


--
-- Name: home_module_permission_codename_9d9bb99a_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX home_module_permission_codename_9d9bb99a_like ON public.home_module USING btree (permission_codename varchar_pattern_ops);


--
-- Name: innovations_innovation_approved_by_id_12837344; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX innovations_innovation_approved_by_id_12837344 ON public.innovations_innovation USING btree (approved_by_id);


--
-- Name: innovations_innovation_court_id_56b3dfaf; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX innovations_innovation_court_id_56b3dfaf ON public.innovations_innovation USING btree (court_id);


--
-- Name: innovations_innovation_financial_year_id_d6222de4; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX innovations_innovation_financial_year_id_d6222de4 ON public.innovations_innovation USING btree (financial_year_id);


--
-- Name: innovations_innovation_submitted_by_id_4ef88a9a; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX innovations_innovation_submitted_by_id_4ef88a9a ON public.innovations_innovation USING btree (submitted_by_id);


--
-- Name: innovations_innovationattachment_innovation_id_54b142fe; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX innovations_innovationattachment_innovation_id_54b142fe ON public.innovations_innovationattachment USING btree (innovation_id);


--
-- Name: innovations_innovationattachment_uploaded_by_id_9dbce7fb; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX innovations_innovationattachment_uploaded_by_id_9dbce7fb ON public.innovations_innovationattachment USING btree (uploaded_by_id);


--
-- Name: mail_mailactivity_mail_id_ed6921bc; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailactivity_mail_id_ed6921bc ON public.mail_mailactivity USING btree (mail_id);


--
-- Name: mail_mailactivity_user_id_265cc658; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailactivity_user_id_265cc658 ON public.mail_mailactivity USING btree (user_id);


--
-- Name: mail_mailassignment_assigned_by_id_b62919b0; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailassignment_assigned_by_id_b62919b0 ON public.mail_mailassignment USING btree (assigned_by_id);


--
-- Name: mail_mailassignment_assigned_to_id_0f8d7452; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailassignment_assigned_to_id_0f8d7452 ON public.mail_mailassignment USING btree (assigned_to_id);


--
-- Name: mail_mailassignment_mail_id_e6c20feb; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailassignment_mail_id_e6c20feb ON public.mail_mailassignment USING btree (mail_id);


--
-- Name: mail_mailattachment_digital_copy_id_6bf09227; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailattachment_digital_copy_id_6bf09227 ON public.mail_mailattachment USING btree (digital_copy_id);


--
-- Name: mail_mailattachment_mail_id_4a0c32b4; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailattachment_mail_id_4a0c32b4 ON public.mail_mailattachment USING btree (mail_id);


--
-- Name: mail_mailmovement_handler_id_e5204da0; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailmovement_handler_id_e5204da0 ON public.mail_mailmovement USING btree (handler_id);


--
-- Name: mail_mailmovement_mail_id_c9da3b50; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_mailmovement_mail_id_c9da3b50 ON public.mail_mailmovement USING btree (mail_id);


--
-- Name: mail_physicalmail_created_by_id_21d60e88; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_physicalmail_created_by_id_21d60e88 ON public.mail_physicalmail USING btree (created_by_id);


--
-- Name: mail_physicalmail_department_id_2c5aba4d; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_physicalmail_department_id_2c5aba4d ON public.mail_physicalmail USING btree (department_id);


--
-- Name: mail_physicalmail_response_mail_id_c56392fa; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_physicalmail_response_mail_id_c56392fa ON public.mail_physicalmail USING btree (response_mail_id);


--
-- Name: mail_physicalmail_tracking_number_e1df731d_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX mail_physicalmail_tracking_number_e1df731d_like ON public.mail_physicalmail USING btree (tracking_number varchar_pattern_ops);


--
-- Name: meetings_meeting_content_type_id_f29520de; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meeting_content_type_id_f29520de ON public.meetings_meeting USING btree (content_type_id);


--
-- Name: meetings_meeting_department_id_4817fabd; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meeting_department_id_4817fabd ON public.meetings_meeting USING btree (department_id);


--
-- Name: meetings_meeting_meeting_type_id_854f500c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meeting_meeting_type_id_854f500c ON public.meetings_meeting USING btree (meeting_type_id);


--
-- Name: meetings_meeting_organizer_id_91f9211b; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meeting_organizer_id_91f9211b ON public.meetings_meeting USING btree (organizer_id);


--
-- Name: meetings_meetingaction_assigned_to_id_6a2f5f16; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meetingaction_assigned_to_id_6a2f5f16 ON public.meetings_meetingaction USING btree (assigned_to_id);


--
-- Name: meetings_meetingaction_meeting_id_3ea63ad4; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meetingaction_meeting_id_3ea63ad4 ON public.meetings_meetingaction USING btree (meeting_id);


--
-- Name: meetings_meetingdocument_document_id_06087c24; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meetingdocument_document_id_06087c24 ON public.meetings_meetingdocument USING btree (document_id);


--
-- Name: meetings_meetingdocument_meeting_id_c9a7951d; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meetingdocument_meeting_id_c9a7951d ON public.meetings_meetingdocument USING btree (meeting_id);


--
-- Name: meetings_meetingparticipant_meeting_id_fb3c3c87; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meetingparticipant_meeting_id_fb3c3c87 ON public.meetings_meetingparticipant USING btree (meeting_id);


--
-- Name: meetings_meetingparticipant_participant_id_665cba69; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX meetings_meetingparticipant_participant_id_665cba69 ON public.meetings_meetingparticipant USING btree (participant_id);


--
-- Name: memos_memo_content_type_id_6164aab3; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_content_type_id_6164aab3 ON public.memos_memo USING btree (content_type_id);


--
-- Name: memos_memo_created_by_id_6a3b0bd2; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_created_by_id_6a3b0bd2 ON public.memos_memo USING btree (created_by_id);


--
-- Name: memos_memo_department_id_e524ae42; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_department_id_e524ae42 ON public.memos_memo USING btree (department_id);


--
-- Name: memos_memo_document_id_6175f414; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_document_id_6175f414 ON public.memos_memo USING btree (document_id);


--
-- Name: memos_memo_recipient_departments_department_id_7ed6ccbc; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_recipient_departments_department_id_7ed6ccbc ON public.memos_memo_recipient_departments USING btree (department_id);


--
-- Name: memos_memo_recipient_departments_memo_id_e41f00ae; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_recipient_departments_memo_id_e41f00ae ON public.memos_memo_recipient_departments USING btree (memo_id);


--
-- Name: memos_memo_recipient_users_customuser_id_44e4d5f9; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_recipient_users_customuser_id_44e4d5f9 ON public.memos_memo_recipient_users USING btree (customuser_id);


--
-- Name: memos_memo_recipient_users_memo_id_a615559a; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_recipient_users_memo_id_a615559a ON public.memos_memo_recipient_users USING btree (memo_id);


--
-- Name: memos_memo_reference_number_14e5f08b_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_reference_number_14e5f08b_like ON public.memos_memo USING btree (reference_number varchar_pattern_ops);


--
-- Name: memos_memo_template_id_cc891411; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memo_template_id_cc891411 ON public.memos_memo USING btree (template_id);


--
-- Name: memos_memoactivity_document_id_13840e02; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoactivity_document_id_13840e02 ON public.memos_memoactivity USING btree (document_id);


--
-- Name: memos_memoactivity_memo_id_eb55111a; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoactivity_memo_id_eb55111a ON public.memos_memoactivity USING btree (memo_id);


--
-- Name: memos_memoactivity_user_id_5e272015; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoactivity_user_id_5e272015 ON public.memos_memoactivity USING btree (user_id);


--
-- Name: memos_memoapproval_approver_id_e2aaebb7; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoapproval_approver_id_e2aaebb7 ON public.memos_memoapproval USING btree (approver_id);


--
-- Name: memos_memoapproval_memo_id_45b7e39d; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoapproval_memo_id_45b7e39d ON public.memos_memoapproval USING btree (memo_id);


--
-- Name: memos_memoapproval_signature_document_id_4e4ade9d; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoapproval_signature_document_id_4e4ade9d ON public.memos_memoapproval USING btree (signature_document_id);


--
-- Name: memos_memocomment_attachments_document_id_689bec97; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memocomment_attachments_document_id_689bec97 ON public.memos_memocomment_attachments USING btree (document_id);


--
-- Name: memos_memocomment_attachments_memocomment_id_70f0cdab; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memocomment_attachments_memocomment_id_70f0cdab ON public.memos_memocomment_attachments USING btree (memocomment_id);


--
-- Name: memos_memocomment_memo_id_2666219b; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memocomment_memo_id_2666219b ON public.memos_memocomment USING btree (memo_id);


--
-- Name: memos_memocomment_parent_id_d3c2dec9; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memocomment_parent_id_d3c2dec9 ON public.memos_memocomment USING btree (parent_id);


--
-- Name: memos_memocomment_user_id_96ee3194; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memocomment_user_id_96ee3194 ON public.memos_memocomment USING btree (user_id);


--
-- Name: memos_memotemplate_created_by_id_bb7b8fa8; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memotemplate_created_by_id_bb7b8fa8 ON public.memos_memotemplate USING btree (created_by_id);


--
-- Name: memos_memotemplate_department_id_f1f14718; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memotemplate_department_id_f1f14718 ON public.memos_memotemplate USING btree (department_id);


--
-- Name: memos_memoversion_created_by_id_dadd57b3; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoversion_created_by_id_dadd57b3 ON public.memos_memoversion USING btree (created_by_id);


--
-- Name: memos_memoversion_document_id_c5cd5f57; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoversion_document_id_c5cd5f57 ON public.memos_memoversion USING btree (document_id);


--
-- Name: memos_memoversion_memo_id_117dc15c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX memos_memoversion_memo_id_117dc15c ON public.memos_memoversion USING btree (memo_id);


--
-- Name: organization_role_department_id_00ba268c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX organization_role_department_id_00ba268c ON public.organization_role USING btree (department_id);


--
-- Name: organization_role_permissions_permission_id_7ba338c8; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX organization_role_permissions_permission_id_7ba338c8 ON public.organization_role_permissions USING btree (permission_id);


--
-- Name: organization_role_permissions_role_id_631f04cb; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX organization_role_permissions_role_id_631f04cb ON public.organization_role_permissions USING btree (role_id);


--
-- Name: organization_userrole_role_id_e39b3251; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX organization_userrole_role_id_e39b3251 ON public.organization_userrole USING btree (role_id);


--
-- Name: organization_userrole_user_id_75e9d758; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX organization_userrole_user_id_75e9d758 ON public.organization_userrole USING btree (user_id);


--
-- Name: pmmu_financialyearperformance_financial_year_id_68f380cc; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_financialyearperformance_financial_year_id_68f380cc ON public.pmmu_financialyearperformance USING btree (financial_year_id);


--
-- Name: pmmu_financialyearperformance_indicator_id_725f87a1; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_financialyearperformance_indicator_id_725f87a1 ON public.pmmu_financialyearperformance USING btree (indicator_id);


--
-- Name: pmmu_indicatorcategory_name_132edb72_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_indicatorcategory_name_132edb72_like ON public.pmmu_indicatorcategory USING btree (name varchar_pattern_ops);


--
-- Name: pmmu_indicatornote_created_by_id_ef20ccb7; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_indicatornote_created_by_id_ef20ccb7 ON public.pmmu_indicatornote USING btree (created_by_id);


--
-- Name: pmmu_indicatornote_indicator_id_394a457f; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_indicatornote_indicator_id_394a457f ON public.pmmu_indicatornote USING btree (indicator_id);


--
-- Name: pmmu_performanceindicator_subcategory_id_ba825997; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_performanceindicator_subcategory_id_ba825997 ON public.pmmu_performanceindicator USING btree (subcategory_id);


--
-- Name: pmmu_pmmu_financial_year_id_b9d609a1; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX pmmu_pmmu_financial_year_id_b9d609a1 ON public.pmmu_pmmu USING btree (financial_year_id);


--
-- Name: statistics_adjournmentreason_unit_rank_id_09b015ba; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_adjournmentreason_unit_rank_id_09b015ba ON public.statistics_adjournmentreason USING btree (unit_rank_id);


--
-- Name: statistics_caseactivitytype_name_bcd7025f_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_caseactivitytype_name_bcd7025f_like ON public.statistics_caseactivitytype USING btree (name varchar_pattern_ops);


--
-- Name: statistics_caseactivitytype_unit_rank_id_acbe8c25; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_caseactivitytype_unit_rank_id_acbe8c25 ON public.statistics_caseactivitytype USING btree (unit_rank_id);


--
-- Name: statistics_casecategory_unit_rank_id_2532592e; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_casecategory_unit_rank_id_2532592e ON public.statistics_casecategory USING btree (unit_rank_id);


--
-- Name: statistics_caseoutcome_unit_rank_id_be448ae4; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_caseoutcome_unit_rank_id_be448ae4 ON public.statistics_caseoutcome USING btree (unit_rank_id);


--
-- Name: statistics_dcrtdata_case_number_code_id_ccef7e22; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_dcrtdata_case_number_code_id_ccef7e22 ON public.statistics_dcrtdata USING btree (case_number_code_id);


--
-- Name: statistics_dcrtdata_division_id_43c50aac; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_dcrtdata_division_id_43c50aac ON public.statistics_dcrtdata USING btree (division_id);


--
-- Name: statistics_dcrtdata_financial_quarter_id_2dc36524; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_dcrtdata_financial_quarter_id_2dc36524 ON public.statistics_dcrtdata USING btree (financial_quarter_id);


--
-- Name: statistics_dcrtdata_financial_year_id_26fa9378; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_dcrtdata_financial_year_id_26fa9378 ON public.statistics_dcrtdata USING btree (financial_year_id);


--
-- Name: statistics_dcrtdata_month_id_dedbca1a; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_dcrtdata_month_id_dedbca1a ON public.statistics_dcrtdata USING btree (month_id);


--
-- Name: statistics_dcrtdata_unit_id_0d093600; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_dcrtdata_unit_id_0d093600 ON public.statistics_dcrtdata USING btree (unit_id);


--
-- Name: statistics_financialquarter_financial_year_id_a2bc4f85; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_financialquarter_financial_year_id_a2bc4f85 ON public.statistics_financialquarter USING btree (financial_year_id);


--
-- Name: statistics_unit_template_unit_id_6b4b044a; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_unit_template_unit_id_6b4b044a ON public.statistics_unit USING btree (template_unit_id);


--
-- Name: statistics_unit_unit_rank_id_e6794cbc; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_unit_unit_rank_id_e6794cbc ON public.statistics_unit USING btree (unit_rank_id);


--
-- Name: statistics_unitdivision_division_id_e1e170b8; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_unitdivision_division_id_e1e170b8 ON public.statistics_unitdivision USING btree (division_id);


--
-- Name: statistics_unitdivision_unit_id_cb0f09bf; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX statistics_unitdivision_unit_id_cb0f09bf ON public.statistics_unitdivision USING btree (unit_id);


--
-- Name: tasks_comment_author_id_096a3bcc; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_comment_author_id_096a3bcc ON public.tasks_comment USING btree (author_id);


--
-- Name: tasks_comment_task_id_8e8bc4fe; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_comment_task_id_8e8bc4fe ON public.tasks_comment USING btree (task_id);


--
-- Name: tasks_project_department_id_6cddf80c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_project_department_id_6cddf80c ON public.tasks_project USING btree (department_id);


--
-- Name: tasks_project_name_5ca69af2_like; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_project_name_5ca69af2_like ON public.tasks_project USING btree (name varchar_pattern_ops);


--
-- Name: tasks_project_owner_id_ce07be61; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_project_owner_id_ce07be61 ON public.tasks_project USING btree (owner_id);


--
-- Name: tasks_task_assignees_customuser_id_8cf1a261; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_task_assignees_customuser_id_8cf1a261 ON public.tasks_task_assignees USING btree (customuser_id);


--
-- Name: tasks_task_assignees_task_id_e57e7ae7; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_task_assignees_task_id_e57e7ae7 ON public.tasks_task_assignees USING btree (task_id);


--
-- Name: tasks_task_content_type_id_90793102; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_task_content_type_id_90793102 ON public.tasks_task USING btree (content_type_id);


--
-- Name: tasks_task_creator_id_ca3b6762; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_task_creator_id_ca3b6762 ON public.tasks_task USING btree (creator_id);


--
-- Name: tasks_task_parent_task_id_7455866c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_task_parent_task_id_7455866c ON public.tasks_task USING btree (parent_task_id);


--
-- Name: tasks_task_project_id_a2815f0c; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_task_project_id_a2815f0c ON public.tasks_task USING btree (project_id);


--
-- Name: tasks_taskhistory_task_id_3c50c29d; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_taskhistory_task_id_3c50c29d ON public.tasks_taskhistory USING btree (task_id);


--
-- Name: tasks_taskhistory_user_id_cc374940; Type: INDEX; Schema: public; Owner: dspop_user
--

CREATE INDEX tasks_taskhistory_user_id_cc374940 ON public.tasks_taskhistory USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authentication_customuser_departments authentication_custo_customuser_id_23099396_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_departments
    ADD CONSTRAINT authentication_custo_customuser_id_23099396_fk_authentic FOREIGN KEY (customuser_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authentication_customuser_user_permissions authentication_custo_customuser_id_33d2a5f7_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_user_permissions
    ADD CONSTRAINT authentication_custo_customuser_id_33d2a5f7_fk_authentic FOREIGN KEY (customuser_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authentication_customuser_groups authentication_custo_customuser_id_a7d1343c_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_groups
    ADD CONSTRAINT authentication_custo_customuser_id_a7d1343c_fk_authentic FOREIGN KEY (customuser_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authentication_customuser_departments authentication_custo_department_id_a87ebd05_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_departments
    ADD CONSTRAINT authentication_custo_department_id_a87ebd05_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authentication_customuser_groups authentication_custo_group_id_c5ef1d10_fk_auth_grou; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_groups
    ADD CONSTRAINT authentication_custo_group_id_c5ef1d10_fk_auth_grou FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authentication_customuser_user_permissions authentication_custo_permission_id_e47332af_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.authentication_customuser_user_permissions
    ADD CONSTRAINT authentication_custo_permission_id_e47332af_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_performanceindicator budget_performancein_workplan_item_id_67607840_fk_budget_wo; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_performanceindicator
    ADD CONSTRAINT budget_performancein_workplan_item_id_67607840_fk_budget_wo FOREIGN KEY (workplan_item_id) REFERENCES public.budget_workplanitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_quarterlyallocation budget_quarterlyallo_workplan_item_id_9abab4fe_fk_budget_wo; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_quarterlyallocation
    ADD CONSTRAINT budget_quarterlyallo_workplan_item_id_9abab4fe_fk_budget_wo FOREIGN KEY (workplan_item_id) REFERENCES public.budget_workplanitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_transformativeinitiative budget_transformativ_workplan_item_id_bd685846_fk_budget_wo; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_transformativeinitiative
    ADD CONSTRAINT budget_transformativ_workplan_item_id_bd685846_fk_budget_wo FOREIGN KEY (workplan_item_id) REFERENCES public.budget_workplanitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_workplanitem budget_workplanitem_category_id_e1a4fd25_fk_budget_bu; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_workplanitem
    ADD CONSTRAINT budget_workplanitem_category_id_e1a4fd25_fk_budget_bu FOREIGN KEY (category_id) REFERENCES public.budget_budgetcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_workplanitem budget_workplanitem_financial_year_id_01db6d20_fk_budget_fi; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.budget_workplanitem
    ADD CONSTRAINT budget_workplanitem_financial_year_id_01db6d20_fk_budget_fi FOREIGN KEY (financial_year_id) REFERENCES public.budget_financialyear(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentcomment document_management__author_id_1723f1a6_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcomment
    ADD CONSTRAINT document_management__author_id_1723f1a6_fk_authentic FOREIGN KEY (author_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_document document_management__category_id_08d18950_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_document
    ADD CONSTRAINT document_management__category_id_08d18950_fk_document_ FOREIGN KEY (category_id) REFERENCES public.document_management_documentcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_document document_management__content_type_id_bfaa50ba_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_document
    ADD CONSTRAINT document_management__content_type_id_bfaa50ba_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentactivity document_management__document_id_460e6b78_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentactivity
    ADD CONSTRAINT document_management__document_id_460e6b78_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentcomment document_management__document_id_68309093_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcomment
    ADD CONSTRAINT document_management__document_id_68309093_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentaccess document_management__document_id_b32bcc6f_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentaccess
    ADD CONSTRAINT document_management__document_id_b32bcc6f_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentaccess document_management__granted_by_id_cf38c85d_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentaccess
    ADD CONSTRAINT document_management__granted_by_id_cf38c85d_fk_authentic FOREIGN KEY (granted_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentcomment document_management__parent_comment_id_e9cd7f2c_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentcomment
    ADD CONSTRAINT document_management__parent_comment_id_e9cd7f2c_fk_document_ FOREIGN KEY (parent_comment_id) REFERENCES public.document_management_documentcomment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_document document_management__parent_document_id_083a3a5f_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_document
    ADD CONSTRAINT document_management__parent_document_id_083a3a5f_fk_document_ FOREIGN KEY (parent_document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_document document_management__uploaded_by_id_7769bbfb_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_document
    ADD CONSTRAINT document_management__uploaded_by_id_7769bbfb_fk_authentic FOREIGN KEY (uploaded_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentactivity document_management__user_id_547c27be_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentactivity
    ADD CONSTRAINT document_management__user_id_547c27be_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_management_documentaccess document_management__user_id_f1c1064b_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.document_management_documentaccess
    ADD CONSTRAINT document_management__user_id_f1c1064b_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: home_module_departments home_module_departme_department_id_1495a1bd_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module_departments
    ADD CONSTRAINT home_module_departme_department_id_1495a1bd_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: home_module_departments home_module_departments_module_id_f6eb1aa1_fk_home_module_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.home_module_departments
    ADD CONSTRAINT home_module_departments_module_id_f6eb1aa1_fk_home_module_id FOREIGN KEY (module_id) REFERENCES public.home_module(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: innovations_innovation innovations_innovati_approved_by_id_12837344_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovation
    ADD CONSTRAINT innovations_innovati_approved_by_id_12837344_fk_authentic FOREIGN KEY (approved_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: innovations_innovation innovations_innovati_financial_year_id_d6222de4_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovation
    ADD CONSTRAINT innovations_innovati_financial_year_id_d6222de4_fk_statistic FOREIGN KEY (financial_year_id) REFERENCES public.statistics_financialyear(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: innovations_innovationattachment innovations_innovati_innovation_id_54b142fe_fk_innovatio; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovationattachment
    ADD CONSTRAINT innovations_innovati_innovation_id_54b142fe_fk_innovatio FOREIGN KEY (innovation_id) REFERENCES public.innovations_innovation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: innovations_innovation innovations_innovati_submitted_by_id_4ef88a9a_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovation
    ADD CONSTRAINT innovations_innovati_submitted_by_id_4ef88a9a_fk_authentic FOREIGN KEY (submitted_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: innovations_innovationattachment innovations_innovati_uploaded_by_id_9dbce7fb_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovationattachment
    ADD CONSTRAINT innovations_innovati_uploaded_by_id_9dbce7fb_fk_authentic FOREIGN KEY (uploaded_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: innovations_innovation innovations_innovation_court_id_56b3dfaf_fk_statistics_unit_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.innovations_innovation
    ADD CONSTRAINT innovations_innovation_court_id_56b3dfaf_fk_statistics_unit_id FOREIGN KEY (court_id) REFERENCES public.statistics_unit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailactivity mail_mailactivity_mail_id_ed6921bc_fk_mail_physicalmail_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailactivity
    ADD CONSTRAINT mail_mailactivity_mail_id_ed6921bc_fk_mail_physicalmail_id FOREIGN KEY (mail_id) REFERENCES public.mail_physicalmail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailactivity mail_mailactivity_user_id_265cc658_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailactivity
    ADD CONSTRAINT mail_mailactivity_user_id_265cc658_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailassignment mail_mailassignment_assigned_by_id_b62919b0_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailassignment
    ADD CONSTRAINT mail_mailassignment_assigned_by_id_b62919b0_fk_authentic FOREIGN KEY (assigned_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailassignment mail_mailassignment_assigned_to_id_0f8d7452_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailassignment
    ADD CONSTRAINT mail_mailassignment_assigned_to_id_0f8d7452_fk_authentic FOREIGN KEY (assigned_to_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailassignment mail_mailassignment_mail_id_e6c20feb_fk_mail_physicalmail_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailassignment
    ADD CONSTRAINT mail_mailassignment_mail_id_e6c20feb_fk_mail_physicalmail_id FOREIGN KEY (mail_id) REFERENCES public.mail_physicalmail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailattachment mail_mailattachment_digital_copy_id_6bf09227_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailattachment
    ADD CONSTRAINT mail_mailattachment_digital_copy_id_6bf09227_fk_document_ FOREIGN KEY (digital_copy_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailattachment mail_mailattachment_mail_id_4a0c32b4_fk_mail_physicalmail_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailattachment
    ADD CONSTRAINT mail_mailattachment_mail_id_4a0c32b4_fk_mail_physicalmail_id FOREIGN KEY (mail_id) REFERENCES public.mail_physicalmail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailmovement mail_mailmovement_handler_id_e5204da0_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailmovement
    ADD CONSTRAINT mail_mailmovement_handler_id_e5204da0_fk_authentic FOREIGN KEY (handler_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_mailmovement mail_mailmovement_mail_id_c9da3b50_fk_mail_physicalmail_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_mailmovement
    ADD CONSTRAINT mail_mailmovement_mail_id_c9da3b50_fk_mail_physicalmail_id FOREIGN KEY (mail_id) REFERENCES public.mail_physicalmail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_physicalmail mail_physicalmail_created_by_id_21d60e88_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_physicalmail
    ADD CONSTRAINT mail_physicalmail_created_by_id_21d60e88_fk_authentic FOREIGN KEY (created_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_physicalmail mail_physicalmail_department_id_2c5aba4d_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_physicalmail
    ADD CONSTRAINT mail_physicalmail_department_id_2c5aba4d_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mail_physicalmail mail_physicalmail_response_mail_id_c56392fa_fk_mail_phys; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.mail_physicalmail
    ADD CONSTRAINT mail_physicalmail_response_mail_id_c56392fa_fk_mail_phys FOREIGN KEY (response_mail_id) REFERENCES public.mail_physicalmail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meeting meetings_meeting_content_type_id_f29520de_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting
    ADD CONSTRAINT meetings_meeting_content_type_id_f29520de_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meeting meetings_meeting_department_id_4817fabd_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting
    ADD CONSTRAINT meetings_meeting_department_id_4817fabd_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meeting meetings_meeting_meeting_type_id_854f500c_fk_meetings_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting
    ADD CONSTRAINT meetings_meeting_meeting_type_id_854f500c_fk_meetings_ FOREIGN KEY (meeting_type_id) REFERENCES public.meetings_meetingtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meeting meetings_meeting_organizer_id_91f9211b_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meeting
    ADD CONSTRAINT meetings_meeting_organizer_id_91f9211b_fk_authentic FOREIGN KEY (organizer_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meetingaction meetings_meetingacti_assigned_to_id_6a2f5f16_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingaction
    ADD CONSTRAINT meetings_meetingacti_assigned_to_id_6a2f5f16_fk_authentic FOREIGN KEY (assigned_to_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meetingaction meetings_meetingacti_meeting_id_3ea63ad4_fk_meetings_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingaction
    ADD CONSTRAINT meetings_meetingacti_meeting_id_3ea63ad4_fk_meetings_ FOREIGN KEY (meeting_id) REFERENCES public.meetings_meeting(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meetingdocument meetings_meetingdocu_document_id_06087c24_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingdocument
    ADD CONSTRAINT meetings_meetingdocu_document_id_06087c24_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meetingdocument meetings_meetingdocu_meeting_id_c9a7951d_fk_meetings_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingdocument
    ADD CONSTRAINT meetings_meetingdocu_meeting_id_c9a7951d_fk_meetings_ FOREIGN KEY (meeting_id) REFERENCES public.meetings_meeting(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meetingparticipant meetings_meetingpart_meeting_id_fb3c3c87_fk_meetings_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingparticipant
    ADD CONSTRAINT meetings_meetingpart_meeting_id_fb3c3c87_fk_meetings_ FOREIGN KEY (meeting_id) REFERENCES public.meetings_meeting(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: meetings_meetingparticipant meetings_meetingpart_participant_id_665cba69_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.meetings_meetingparticipant
    ADD CONSTRAINT meetings_meetingpart_participant_id_665cba69_fk_authentic FOREIGN KEY (participant_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo memos_memo_content_type_id_6164aab3_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_content_type_id_6164aab3_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo memos_memo_created_by_id_6a3b0bd2_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_created_by_id_6a3b0bd2_fk_authentic FOREIGN KEY (created_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo memos_memo_department_id_e524ae42_fk_organization_department_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_department_id_e524ae42_fk_organization_department_id FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo memos_memo_document_id_6175f414_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_document_id_6175f414_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo_recipient_users memos_memo_recipient_customuser_id_44e4d5f9_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_users
    ADD CONSTRAINT memos_memo_recipient_customuser_id_44e4d5f9_fk_authentic FOREIGN KEY (customuser_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo_recipient_departments memos_memo_recipient_department_id_7ed6ccbc_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_departments
    ADD CONSTRAINT memos_memo_recipient_department_id_7ed6ccbc_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo_recipient_departments memos_memo_recipient_memo_id_e41f00ae_fk_memos_mem; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_departments
    ADD CONSTRAINT memos_memo_recipient_memo_id_e41f00ae_fk_memos_mem FOREIGN KEY (memo_id) REFERENCES public.memos_memo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo_recipient_users memos_memo_recipient_users_memo_id_a615559a_fk_memos_memo_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo_recipient_users
    ADD CONSTRAINT memos_memo_recipient_users_memo_id_a615559a_fk_memos_memo_id FOREIGN KEY (memo_id) REFERENCES public.memos_memo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memo memos_memo_template_id_cc891411_fk_memos_memotemplate_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memo
    ADD CONSTRAINT memos_memo_template_id_cc891411_fk_memos_memotemplate_id FOREIGN KEY (template_id) REFERENCES public.memos_memotemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoactivity memos_memoactivity_document_id_13840e02_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoactivity
    ADD CONSTRAINT memos_memoactivity_document_id_13840e02_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoactivity memos_memoactivity_memo_id_eb55111a_fk_memos_memo_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoactivity
    ADD CONSTRAINT memos_memoactivity_memo_id_eb55111a_fk_memos_memo_id FOREIGN KEY (memo_id) REFERENCES public.memos_memo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoactivity memos_memoactivity_user_id_5e272015_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoactivity
    ADD CONSTRAINT memos_memoactivity_user_id_5e272015_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoapproval memos_memoapproval_approver_id_e2aaebb7_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoapproval
    ADD CONSTRAINT memos_memoapproval_approver_id_e2aaebb7_fk_authentic FOREIGN KEY (approver_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoapproval memos_memoapproval_memo_id_45b7e39d_fk_memos_memo_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoapproval
    ADD CONSTRAINT memos_memoapproval_memo_id_45b7e39d_fk_memos_memo_id FOREIGN KEY (memo_id) REFERENCES public.memos_memo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoapproval memos_memoapproval_signature_document_i_4e4ade9d_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoapproval
    ADD CONSTRAINT memos_memoapproval_signature_document_i_4e4ade9d_fk_document_ FOREIGN KEY (signature_document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memocomment_attachments memos_memocomment_at_document_id_689bec97_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment_attachments
    ADD CONSTRAINT memos_memocomment_at_document_id_689bec97_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memocomment_attachments memos_memocomment_at_memocomment_id_70f0cdab_fk_memos_mem; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment_attachments
    ADD CONSTRAINT memos_memocomment_at_memocomment_id_70f0cdab_fk_memos_mem FOREIGN KEY (memocomment_id) REFERENCES public.memos_memocomment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memocomment memos_memocomment_memo_id_2666219b_fk_memos_memo_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment
    ADD CONSTRAINT memos_memocomment_memo_id_2666219b_fk_memos_memo_id FOREIGN KEY (memo_id) REFERENCES public.memos_memo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memocomment memos_memocomment_parent_id_d3c2dec9_fk_memos_memocomment_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment
    ADD CONSTRAINT memos_memocomment_parent_id_d3c2dec9_fk_memos_memocomment_id FOREIGN KEY (parent_id) REFERENCES public.memos_memocomment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memocomment memos_memocomment_user_id_96ee3194_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memocomment
    ADD CONSTRAINT memos_memocomment_user_id_96ee3194_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memotemplate memos_memotemplate_created_by_id_bb7b8fa8_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memotemplate
    ADD CONSTRAINT memos_memotemplate_created_by_id_bb7b8fa8_fk_authentic FOREIGN KEY (created_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memotemplate memos_memotemplate_department_id_f1f14718_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memotemplate
    ADD CONSTRAINT memos_memotemplate_department_id_f1f14718_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoversion memos_memoversion_created_by_id_dadd57b3_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoversion
    ADD CONSTRAINT memos_memoversion_created_by_id_dadd57b3_fk_authentic FOREIGN KEY (created_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoversion memos_memoversion_document_id_c5cd5f57_fk_document_; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoversion
    ADD CONSTRAINT memos_memoversion_document_id_c5cd5f57_fk_document_ FOREIGN KEY (document_id) REFERENCES public.document_management_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: memos_memoversion memos_memoversion_memo_id_117dc15c_fk_memos_memo_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.memos_memoversion
    ADD CONSTRAINT memos_memoversion_memo_id_117dc15c_fk_memos_memo_id FOREIGN KEY (memo_id) REFERENCES public.memos_memo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: organization_role organization_role_department_id_00ba268c_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role
    ADD CONSTRAINT organization_role_department_id_00ba268c_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: organization_role_permissions organization_role_pe_permission_id_7ba338c8_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role_permissions
    ADD CONSTRAINT organization_role_pe_permission_id_7ba338c8_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: organization_role_permissions organization_role_pe_role_id_631f04cb_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_role_permissions
    ADD CONSTRAINT organization_role_pe_role_id_631f04cb_fk_organizat FOREIGN KEY (role_id) REFERENCES public.organization_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: organization_userrole organization_userrol_user_id_75e9d758_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_userrole
    ADD CONSTRAINT organization_userrol_user_id_75e9d758_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: organization_userrole organization_userrole_role_id_e39b3251_fk_organization_role_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.organization_userrole
    ADD CONSTRAINT organization_userrole_role_id_e39b3251_fk_organization_role_id FOREIGN KEY (role_id) REFERENCES public.organization_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pmmu_financialyearperformance pmmu_financialyearpe_financial_year_id_68f380cc_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_financialyearperformance
    ADD CONSTRAINT pmmu_financialyearpe_financial_year_id_68f380cc_fk_statistic FOREIGN KEY (financial_year_id) REFERENCES public.statistics_financialyear(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pmmu_financialyearperformance pmmu_financialyearpe_indicator_id_725f87a1_fk_pmmu_perf; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_financialyearperformance
    ADD CONSTRAINT pmmu_financialyearpe_indicator_id_725f87a1_fk_pmmu_perf FOREIGN KEY (indicator_id) REFERENCES public.pmmu_performanceindicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pmmu_indicatornote pmmu_indicatornote_created_by_id_ef20ccb7_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatornote
    ADD CONSTRAINT pmmu_indicatornote_created_by_id_ef20ccb7_fk_authentic FOREIGN KEY (created_by_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pmmu_indicatornote pmmu_indicatornote_indicator_id_394a457f_fk_pmmu_perf; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_indicatornote
    ADD CONSTRAINT pmmu_indicatornote_indicator_id_394a457f_fk_pmmu_perf FOREIGN KEY (indicator_id) REFERENCES public.pmmu_performanceindicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pmmu_performanceindicator pmmu_performanceindi_subcategory_id_ba825997_fk_pmmu_indi; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_performanceindicator
    ADD CONSTRAINT pmmu_performanceindi_subcategory_id_ba825997_fk_pmmu_indi FOREIGN KEY (subcategory_id) REFERENCES public.pmmu_indicatorcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pmmu_pmmu pmmu_pmmu_financial_year_id_b9d609a1_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.pmmu_pmmu
    ADD CONSTRAINT pmmu_pmmu_financial_year_id_b9d609a1_fk_statistic FOREIGN KEY (financial_year_id) REFERENCES public.statistics_financialyear(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_adjournmentreason statistics_adjournme_unit_rank_id_09b015ba_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_adjournmentreason
    ADD CONSTRAINT statistics_adjournme_unit_rank_id_09b015ba_fk_statistic FOREIGN KEY (unit_rank_id) REFERENCES public.statistics_unitrank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_caseactivitytype statistics_caseactiv_unit_rank_id_acbe8c25_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseactivitytype
    ADD CONSTRAINT statistics_caseactiv_unit_rank_id_acbe8c25_fk_statistic FOREIGN KEY (unit_rank_id) REFERENCES public.statistics_unitrank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_casecategory statistics_casecateg_unit_rank_id_2532592e_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_casecategory
    ADD CONSTRAINT statistics_casecateg_unit_rank_id_2532592e_fk_statistic FOREIGN KEY (unit_rank_id) REFERENCES public.statistics_unitrank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_caseoutcome statistics_caseoutco_unit_rank_id_be448ae4_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_caseoutcome
    ADD CONSTRAINT statistics_caseoutco_unit_rank_id_be448ae4_fk_statistic FOREIGN KEY (unit_rank_id) REFERENCES public.statistics_unitrank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_dcrtdata statistics_dcrtdata_case_number_code_id_ccef7e22_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_case_number_code_id_ccef7e22_fk_statistic FOREIGN KEY (case_number_code_id) REFERENCES public.statistics_casecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_dcrtdata statistics_dcrtdata_division_id_43c50aac_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_division_id_43c50aac_fk_statistic FOREIGN KEY (division_id) REFERENCES public.statistics_division(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_dcrtdata statistics_dcrtdata_financial_quarter_id_2dc36524_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_financial_quarter_id_2dc36524_fk_statistic FOREIGN KEY (financial_quarter_id) REFERENCES public.statistics_financialquarter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_dcrtdata statistics_dcrtdata_financial_year_id_26fa9378_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_financial_year_id_26fa9378_fk_statistic FOREIGN KEY (financial_year_id) REFERENCES public.statistics_financialyear(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_dcrtdata statistics_dcrtdata_month_id_dedbca1a_fk_statistics_months_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_month_id_dedbca1a_fk_statistics_months_id FOREIGN KEY (month_id) REFERENCES public.statistics_months(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_dcrtdata statistics_dcrtdata_unit_id_0d093600_fk_statistics_unit_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_dcrtdata
    ADD CONSTRAINT statistics_dcrtdata_unit_id_0d093600_fk_statistics_unit_id FOREIGN KEY (unit_id) REFERENCES public.statistics_unit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_financialquarter statistics_financial_financial_year_id_a2bc4f85_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_financialquarter
    ADD CONSTRAINT statistics_financial_financial_year_id_a2bc4f85_fk_statistic FOREIGN KEY (financial_year_id) REFERENCES public.statistics_financialyear(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_unit statistics_unit_template_unit_id_6b4b044a_fk_statistics_unit_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unit
    ADD CONSTRAINT statistics_unit_template_unit_id_6b4b044a_fk_statistics_unit_id FOREIGN KEY (template_unit_id) REFERENCES public.statistics_unit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_unit statistics_unit_unit_rank_id_e6794cbc_fk_statistics_unitrank_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unit
    ADD CONSTRAINT statistics_unit_unit_rank_id_e6794cbc_fk_statistics_unitrank_id FOREIGN KEY (unit_rank_id) REFERENCES public.statistics_unitrank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_unitdivision statistics_unitdivis_division_id_e1e170b8_fk_statistic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unitdivision
    ADD CONSTRAINT statistics_unitdivis_division_id_e1e170b8_fk_statistic FOREIGN KEY (division_id) REFERENCES public.statistics_division(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: statistics_unitdivision statistics_unitdivision_unit_id_cb0f09bf_fk_statistics_unit_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.statistics_unitdivision
    ADD CONSTRAINT statistics_unitdivision_unit_id_cb0f09bf_fk_statistics_unit_id FOREIGN KEY (unit_id) REFERENCES public.statistics_unit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_comment tasks_comment_author_id_096a3bcc_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_comment
    ADD CONSTRAINT tasks_comment_author_id_096a3bcc_fk_authentic FOREIGN KEY (author_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_comment tasks_comment_task_id_8e8bc4fe_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_comment
    ADD CONSTRAINT tasks_comment_task_id_8e8bc4fe_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_project tasks_project_department_id_6cddf80c_fk_organizat; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_project
    ADD CONSTRAINT tasks_project_department_id_6cddf80c_fk_organizat FOREIGN KEY (department_id) REFERENCES public.organization_department(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_project tasks_project_owner_id_ce07be61_fk_authentication_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_project
    ADD CONSTRAINT tasks_project_owner_id_ce07be61_fk_authentication_customuser_id FOREIGN KEY (owner_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_assignees tasks_task_assignees_customuser_id_8cf1a261_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task_assignees
    ADD CONSTRAINT tasks_task_assignees_customuser_id_8cf1a261_fk_authentic FOREIGN KEY (customuser_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_assignees tasks_task_assignees_task_id_e57e7ae7_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task_assignees
    ADD CONSTRAINT tasks_task_assignees_task_id_e57e7ae7_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_content_type_id_90793102_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_content_type_id_90793102_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_creator_id_ca3b6762_fk_authentication_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_creator_id_ca3b6762_fk_authentication_customuser_id FOREIGN KEY (creator_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_parent_task_id_7455866c_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_parent_task_id_7455866c_fk_tasks_task_id FOREIGN KEY (parent_task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_project_id_a2815f0c_fk_tasks_project_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_project_id_a2815f0c_fk_tasks_project_id FOREIGN KEY (project_id) REFERENCES public.tasks_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_taskhistory tasks_taskhistory_task_id_3c50c29d_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_taskhistory
    ADD CONSTRAINT tasks_taskhistory_task_id_3c50c29d_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_taskhistory tasks_taskhistory_user_id_cc374940_fk_authentic; Type: FK CONSTRAINT; Schema: public; Owner: dspop_user
--

ALTER TABLE ONLY public.tasks_taskhistory
    ADD CONSTRAINT tasks_taskhistory_user_id_cc374940_fk_authentic FOREIGN KEY (user_id) REFERENCES public.authentication_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--


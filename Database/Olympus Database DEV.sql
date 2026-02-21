-- ==========================================
-- 0. DEVELOPMENT RESET (Clean Slate)
-- ==========================================
-- We use CASCADE to ensure all tables, constraints, and data are wiped.
DROP SCHEMA IF EXISTS "charon" CASCADE;
DROP SCHEMA IF EXISTS "athena" CASCADE;
DROP SCHEMA IF EXISTS "themis" CASCADE;
DROP SCHEMA IF EXISTS "argus" CASCADE;
DROP SCHEMA IF EXISTS "hermes" CASCADE;
-- We don't drop 'public' because it contains system extensions, 
-- but we drop the specific tables if they exist.
DROP TABLE IF EXISTS "public"."staff" CASCADE;
DROP TABLE IF EXISTS "public"."members" CASCADE;

-- ==========================================
-- 1. SCHEMAS
-- ==========================================
CREATE SCHEMA IF NOT EXISTS "charon"; -- Adding a "charon" schema to the database
CREATE SCHEMA IF NOT EXISTS "athena"; -- Adding a "athena" schema to the database (Wisdom & Quests)
CREATE SCHEMA IF NOT EXISTS "themis"; -- Adding a "themis" schema to the database (Law & Penalties)
CREATE SCHEMA IF NOT EXISTS "argus";  -- Adding a "argus" schema to the database (Security)
CREATE SCHEMA IF NOT EXISTS "hermes"; -- Adding a "hermes" schema to the database (Support & Tickets)

-- ==========================================
-- 2. CHARON (Verification)
-- ==========================================
CREATE TABLE "charon"."verficationLogs"(
    "discord_id" BIGINT NOT NULL PRIMARY KEY, --Member's discord ID
    "gatePassedAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, --The timestamp that the member was verified at
    "invitiedBy" BIGINT NOT NULL, --Which mod verified him
    "watchlistStatus" BOOLEAN NOT NULL, --Is this member suspicious, should they be put on a watchlist?
    "archivedAt" TIMESTAMP(0) NULL -- Soft delete for verification records
);

-- ==========================================
-- 3. THEMIS (Law)
-- ==========================================
CREATE TABLE "themis"."penalties"(
    "id" BIGSERIAL NOT NULL PRIMARY KEY, --A unique identifier for each different penalty
    "targetID" BIGINT NOT NULL, --The member that got the penalty
    "ruleBreakID" BIGINT NOT NULL, --Which rule break is the strike from? Should we remove this since it was built for Oxy Archive?
    "issuedBy" BIGINT NOT NULL, --Which mod issued the penalty?
    "messageLink" TEXT NOT NULL, --Message link that goes to the message where the cause of the penalty occured
    "status" VARCHAR(255) CHECK ("status" IN('Active', 'Expired', 'Appealed')) NOT NULL, --The status of the penalty
    "archivedAt" TIMESTAMP(0) NULL -- Hides old/irrelevant penalty records
);

CREATE TABLE "themis"."penaltyTypes"(
    "id" BIGSERIAL NOT NULL PRIMARY KEY, --A unique number assinged to each penalty type
    "name" VARCHAR(255) NOT NULL, --The name of the penalty type
    "description" TEXT NOT NULL, --A description to elaborate on the penalty type
    "durationHours" INTEGER NOT NULL DEFAULT 0, --If there is a mute/timeout how long does it last?
    "escalationLevel" INTEGER NOT NULL, --What level of strike is this?
    "actionToBeTaken" TEXT NOT NULL,--What appropriate action needs to be taken about this penalty type with this escalation level
    "archivedAt" TIMESTAMP(0) NULL -- Retires old penalty types without breaking history
);

CREATE TABLE "themis"."evidenceLinks"(
    "evidenceID" BIGSERIAL NOT NULL PRIMARY KEY, --Unique ID for every single link
    "penaltyID" BIGINT NOT NULL, --The penalty this link belongs to
    "link" TEXT NOT NULL, --The single URL/link of the discord embeded images
    "uploadedBy" BIGINT NOT NULL, --Tracks exactly which mod provided this specific proof
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, -- When this proof was added
    "archivedAt" TIMESTAMP(0) NULL -- Archives specific evidence
);

-- ==========================================
-- 4. PUBLIC (Identity)
-- ==========================================
CREATE TABLE "public"."members"(
    "discordID" BIGINT NOT NULL PRIMARY KEY, --The member's discord ID
    "memberUsername" TEXT NOT NULL, --The member's username
    "firstSeen" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, --When the member joined the server
    "timeLeft" BIGINT NULL, --When the member left the server
    "archivedAt" TIMESTAMP(0) NULL -- Marks a member as "Left" or "Inactive"
);

CREATE TABLE "public"."staff"(
    "discordID" BIGINT NOT NULL PRIMARY KEY, --Staff Member's discord ID
    "username" TEXT NOT NULL, --Staff Member's username
    "department" VARCHAR(255) CHECK -- What department is the staff member in
        (
            "department" IN('General', 'Contest/Event', 'Roleplay', 'Minecraft', 'Verfication/Ticket', 'Dailies')
        ) NOT NULL,
    "rank" VARCHAR(255) CHECK --What rank is this mod, is he a full fledged mod? A mod with seniority? Or an admin?
        (
            "rank" IN('Admin', 'Trial', 'Senior', 'Full Fledged Mod')
        ) NOT NULL,
    "isOnTrial" BOOLEAN NOT NULL, --A boolean check if the staff member is a trail mod or not
    "trailStartAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, --If they're a trail mod, when did their trail start?
    "promotedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL, --When where they promoted from trail mod into a fully fledged mod
    "archivedAt" TIMESTAMP(0) NULL -- Archives staff members (The "Hall of Heroes" logic)
);

-- Key-Value style table.
CREATE TABLE IF NOT EXISTS "public"."settings" (
    "settingKey" TEXT PRIMARY KEY, --The variable name that needs to be stored
    "settingValue" TEXT NOT NULL,  --The variable's value
    "description" TEXT, --A text description that explains this variable and it's value
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP --When was the last time this variable's value was updated
);

-- ==========================================
-- 5. ATHENA (Quests & Favour)
-- ==========================================
CREATE TABLE "athena"."quests"(
    "id" BIGSERIAL NOT NULL PRIMARY KEY, --The unique identifier of this task.
    "title" TEXT NOT NULL, --The title of the task
    "description" TEXT NOT NULL, --The task description
    "assignedRole" VARCHAR(255) CHECK -- This is the variable that's gonna see what mod category or admin this quest should be assigned to what quest pool
        ("assignedRole" IN('General', 'Contest/Event', 'Roleplay', 'Minecraft', 'Verfication/Ticket', 'Dailies', 'Admin')) NOT NULL, -- I Need to double check the mod category quest pools here
    "frequency" VARCHAR(255) -- How frequent is this quest gonna, a one-time thing? Daily? Weekly?
    CHECK
        ("frequency" IN('Daily', 'Weekly', 'One-Time')) NOT NULL,
    "points" BIGINT NOT NULL, -- How many points does completing this quest accomplish. (The ammount of "Favour with the Gods")
    "archivedAt" TIMESTAMP(0) NULL -- Removes quests from the active pool
);

CREATE TABLE "athena"."questLogs"(
    "id" BIGSERIAL NOT NULL PRIMARY KEY, -- Unique id for every completion
    "staffID" BIGINT NOT NULL, --What
    "questID" BIGINT NOT NULL,
    "completedAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "archivedAt" TIMESTAMP(0) NULL -- Archives historical completion logs
);

CREATE TABLE "athena"."lexicon"(
    "key" BIGINT NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "archivedAt" TIMESTAMP(0) NULL -- Soft delete for dictionary/rules entries
);

CREATE TABLE "athena"."completeLogOfFavour"(
    "staffID" BIGINT NOT NULL PRIMARY KEY, -- A staff member's discord ID
    "totalFavour" BIGINT NOT NULL, -- The staff member's current favour (aka their current balance)
    "liftimeEarned" BIGINT NOT NULL, -- A permanent counter that only goes up (for "All Time" Hall of Fame stats)
    "lastUpdated" BIGINT NOT NULL,
    "highScore" BIGINT NOT NULL, -- The staff member's high score that they ever achieved
    "archivedAt" TIMESTAMP(0) NULL -- Archives the entire point balance for a user
);

CREATE TABLE "athena"."ledger"(
    "id" BIGSERIAL NOT NULL PRIMARY KEY, --An autoincrement value that uniquely identifies each ledger update
    "amount" BIGINT NOT NULL, --Tracks favour increase/decrease for a row/record
    "targetStaffID" BIGINT NOT NULL, --Which staff member was affected in this record
    "type" VARCHAR(255) CHECK --How was this record applied? Was it by a Super Admin? A penalty for missing a daily?
        ("type" IN('Quest', 'Penalty', 'Manual', 'Auto-Deduction')) NOT NULL,
    "reason" TEXT NOT NULL, --The reason for this record
    "issuedBy" BIGINT DEFAULT 0, --Who issued this record? [0 represents 'The System']
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, --When was this record created?
    "archivedAt" TIMESTAMP(0) NULL -- Archives specific bank transactions
);

-- ==========================================
-- 6. ARGUS (Security)
-- ==========================================
CREATE TABLE "argus"."incidentReports"(
    "incidentID" BIGSERIAL NOT NULL PRIMARY KEY, --A unique autoincrementing id to identify this report
    "channelID" BIGINT NOT NULL, --Which channel did this occur?
    "threatLevel" INTEGER NOT NULL, -- A value between 1 and 10 determined by the AI
    "summary" TEXT NOT NULL, -- An AI-generated snippet of why it's flagged
    "actionTaken" TEXT NOT NULL, -- Maybe make it an enum?? Ex: Silent Ping Sent, Admin Notified
    "archivedAt" TIMESTAMP(0) NULL -- Hides old incident alerts
);

CREATE TABLE "argus"."watchlist"(
    "discordID" BIGINT NOT NULL PRIMARY KEY, --The member discord ID that are on the watchlist and that need to be monitored
    "numOfMessagesSent" BIGINT NOT NULL, --How many messages did this member send to track if this member is active or not.
    "archivedAt" TIMESTAMP(0) NULL -- Removes someone from the active watchlist
);

-- ==========================================
-- 7. HERMES (Support)
-- ==========================================
CREATE TABLE "hermes"."tickets"(
    "id" BIGSERIAL NOT NULL PRIMARY KEY, --An autoincrmenting value that differentiates each ticket (Kind of like a ticket number)
    "creatorID" BIGINT NOT NULL, --This value tracks who created the ticket
    "category" VARCHAR(255) CHECK -- This holds all the categories that a ticket can be
        (
            "category" IN('Scamming', 'Verfication', 'Report a member', 'Suggestions', 'Partnership', 'Technical Issues', 'Report a rule-break', 'Report a mod', 'Report an admin')
        ) NOT NULL,
    "assignedStaff" BIGINT NOT NULL, --Who was assigned to the ticket or who claimed it?
    "status" VARCHAR(255) CHECK ("status" IN('Open', 'Pending', 'Resolved')) NOT NULL, --THe status of the ticket, is it open, pending or closed?
    "archivedAt" TIMESTAMP(0) NULL -- Archives old support tickets
);

CREATE TABLE "hermes"."feedback"(
    "ticketID" BIGINT NOT NULL PRIMARY KEY, --This links to a ticketID so it's relational
    "rating" VARCHAR(255) CHECK  --What rating does the member give his ticket experience?
        ("rating" IN('0','1','2','3','4','5','6','7','8','9','10')) NOT NULL,
    "comments" TEXT NOT NULL, --A member can leave a comment about their ticket experience and can express any feedback they have about the mod who helped them
    "archivedAt" TIMESTAMP(0) NULL -- Archives feedback entries
);

-- ==========================================
-- 8. INITIALIZATION (The System Gods)
-- ==========================================
-- Create the "System" identity in the members table first (due to FK logic)
INSERT INTO "public"."members" ("discordID", "memberUsername", "firstSeen")
VALUES (0, 'SYSTEM_ENTITY', CURRENT_TIMESTAMP)
ON CONFLICT ("discordID") DO NOTHING;

-- Create the "System" staff account
INSERT INTO "public"."staff" (
    "discordID", 
    "username", 
    "department", 
    "rank", 
    "isOnTrial", 
    "trailStartAt"
)
VALUES (
    0, 
    'The System', 
    'General', 
    'Admin', 
    false, 
    CURRENT_TIMESTAMP
)
ON CONFLICT ("discordID") DO NOTHING;


-- ==========================================
-- 9. RELATIONS (Foreign Keys)
-- ==========================================
ALTER TABLE "public"."staff" ADD CONSTRAINT "fk_staff_member" FOREIGN KEY ("discordID") REFERENCES "public"."members" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "themis"."penalties" ADD CONSTRAINT "fk_penalty_target" FOREIGN KEY ("targetID") REFERENCES "public"."members" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "themis"."penalties" ADD CONSTRAINT "fk_penalty_rule" FOREIGN KEY ("ruleBreakID") REFERENCES "themis"."penaltyTypes" ("id") ON DELETE RESTRICT;
ALTER TABLE "themis"."penalties" ADD CONSTRAINT "fk_penalty_issuer" FOREIGN KEY ("issuedBy") REFERENCES "public"."staff" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "themis"."evidenceLinks" ADD CONSTRAINT "fk_evidence_penalty" FOREIGN KEY ("penaltyID") REFERENCES "themis"."penalties" ("id") ON DELETE RESTRICT;
ALTER TABLE "themis"."evidenceLinks" ADD CONSTRAINT "fk_evidence_uploader" FOREIGN KEY ("uploadedBy") REFERENCES "public"."staff" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "athena"."ledger" ADD CONSTRAINT "fk_ledger_target" FOREIGN KEY ("targetStaffID") REFERENCES "public"."staff" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "athena"."ledger" ADD CONSTRAINT "fk_ledger_issuer" FOREIGN KEY ("issuedBy") REFERENCES "public"."staff" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "athena"."questLogs" ADD CONSTRAINT "fk_quest_log_staff" FOREIGN KEY ("staffID") REFERENCES "public"."staff" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "athena"."questLogs" ADD CONSTRAINT "fk_quest_log_quest" FOREIGN KEY ("questID") REFERENCES "athena"."quests" ("id") ON DELETE RESTRICT;
ALTER TABLE "hermes"."tickets" ADD CONSTRAINT "fk_ticket_creator" FOREIGN KEY ("creatorID") REFERENCES "public"."members" ("discordID") ON DELETE RESTRICT;
ALTER TABLE "hermes"."feedback" ADD CONSTRAINT "fk_feedback_ticket" FOREIGN KEY ("ticketID") REFERENCES "hermes"."tickets" ("id") ON DELETE RESTRICT;
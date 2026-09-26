---
name: project-scaffolding
description: Set up a new project's directory structure and boilerplate following the real convention for its language/framework/deliverable type, rather than an invented ad hoc layout. Use whenever starting a new project or repo, adding a module that needs its own structural convention, or restructuring an existing messy layout. Covers single packages, applications, services, and monorepos.
---

# Project Scaffolding

A scaffold invented from habit instead of from the ecosystem's actual convention costs the project every time a new contributor or tool (a linter, a build system, a package registry) expects the structure it's used to and doesn't find it. This skill scaffolds to the real convention, and states which one it's following.

## Step 1 — Identify the actual project type first

The correct scaffold depends on more than the language: a library has different needs than an application; a single service is structured differently from a monorepo; a CLI tool differs from a long-running service. Get this right before creating a single directory — the "generic" scaffold that ignores this distinction is wrong for most of the specific cases it gets applied to.

## Step 2 — Follow the ecosystem's real convention, and say which one

Use the layout the language/framework's own tooling and community actually expect (for example: a Python package's expected `src/` layout and packaging metadata file, a Node project's expected manifest and source/output separation, a Go module's expected command/internal package conventions, a framework's own CLI-generated structure where one exists). State explicitly which convention is being followed and why — presenting an idiosyncratic structure as if it's the standard one misleads anyone who later assumes it behaves like a familiar project of that type.

## Step 3 — Separate concerns clearly

Source, tests, configuration, build output, and documentation each get their own place, not commingled. Make sure `.gitignore` matches — build/artifact directories excluded from version control (see `github-master`'s guidance on not committing generated artifacts).

## Step 4 — Minimum viable boilerplate, not maximum

Include what a project of this type actually needs immediately: a README stub, a license placeholder if the project needs one, a CI config skeleton if requested, and an example/template config file (`.env.example`, not a real `.env` with committed secrets) rather than committing actual configuration values. Don't create directories "for future use" that will sit empty for months — an empty placeholder folder adds noise to the structure without adding actual organization value; add it when there's real content for it, not before.

## Step 5 — For a monorepo or multi-package layout, state the boundary explicitly

Name what's shared across packages versus what's private to one, and the convention for how packages depend on each other. This is the scaffolding decision that's hardest to change later, so it deserves being stated explicitly up front rather than left implicit in whatever the first two packages happened to do.

## Step 6 — Restructuring an existing project is a migration, not a silent rewrite

State the plan (what moves where) before executing it. Move files with `git mv` rather than delete-and-recreate where possible, so version control tracks the change as a rename and the file's history follows it rather than appearing to start fresh (ties into `github-master`'s commit-quality guidance on keeping history useful).

## Output

State the project type identified, the convention being followed and why, the directory tree actually created, and which parts are functional immediately versus placeholders awaiting real content.

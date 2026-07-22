# Tiny World Builder collaboration and deployment glossary

## ADR

Architecture Decision Record. A short document that captures a significant
technical or process decision, its context, and its consequences.

## CCUIS

Conversational Compute User Interface Surface. The collaboration and interface
layer through which humans and AI systems coordinate work and manage cognitive
load.

## GFSM

Goal Finite-State Machine. A lightweight goal-tracking model using identifiers
such as `G_001` and state markers like `+`, `?`, `-`, `!`, `*`, and `_` to show
whether a goal is active, proposed, shelved, blocked, ongoing, or done.

## Keep a Changelog

A changelog structure that groups release notes into sections such as Added,
Changed, Fixed, and Removed.

## Long-lived overlay branch

A branch intended to exist for an extended period as a stable layer on top of
another branch. In this repo, `domains/*` branches are long-lived overlays on
`main`.

## PRD

Product Requirements Document. A document that defines a milestone's problem,
goals, users, scope, constraints, and success criteria.

## PromptVer-TDD

Prompt Versioning and Test-Driven Development. A framework that treats prompt
engineering as an iterative engineering discipline with versioning, simulation,
reflection, and refinement loops.

## Sentinel prefix

A naming prefix with operational meaning. In this repo, `domains/` is the
sentinel prefix that marks a branch as a private deployment overlay.

## Single-writer rule

An operational rule that only one human or automation agent may apply live
infrastructure changes at a time.

## SNEng

Solutions Negation Engineering. A deliberate review technique that records what
not to do so likely failure modes are made explicit before execution.

## Stigmergy

Indirect collaboration through shared artifacts. In this repo, ADRs, PRDs,
issue drafts, workflow files, and other committed documents form part of the
stigmergic collaboration surface for humans and AI agents.

## Upstream-clean `main`

A policy that the fork's `main` branch should remain realistic to merge or
cherry-pick into upstream without carrying fork-private infrastructure details.

## Wildcard preview domain

A subdomain pattern such as `*.example.dev` used to route many preview hosts. In
this project, wildcard previews are a later milestone and are separate from the
first canonical deployment hostname.

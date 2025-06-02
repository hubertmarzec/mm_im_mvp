# Testing Strategy for Classification and Extraction API

## 1. Overview

This document outlines the comprehensive testing strategy for our classification and extraction API system, focusing on user-centric requirements and framework capabilities that enable efficient testing across all levels.

## 2. User Stories & Requirements

### 2.1 Data Management
- **US-001**: As QA and Developer, I want to easily share test data between different test types (unit, functional, integration, e2e)
- **US-002**: As QA, I want to execute e2e tests on synthetic/anonymized data stored in repository or with prod data stored remotely on Databricks volume

### 2.2 Test Execution & Usability
- **US-003**: As QA, I want to easily create e2e tests focusing only on the tests, not the testing framework code
- **US-004**: As Developer, I want to be able to run e2e tests
- **US-005**: As QA, I want to store test execution results in format/form which can be easily transformed later as evidence

### 2.3 Domain-Specific Testing
- **US-006**: As QA, I want to perform e2e testing of the API for classification and extraction data from uploaded files with:
  - POST /request receiving 2 files: `image.tiff`, `result.xml`, returns requestId
  - Async processing (~1min duration)
  - Separate endpoint  GET /request/{requestId} for classification results - many documents
  - Manual classification POST /request/{requesetId}/classificationManualFeeadback 2 files:  `new_mage.tiff`, `new_result.xml`
  - Async processing Type-specific async extraction per document type
  - Sepatate endpoint for extraction results GET /request/{requestId}/{type}-{index}/extraction
  - Manual extraction POST /request/{requesetId}/extractionManualFeeadback 2 files:  `last_mage.tiff`, `last_result.xml`




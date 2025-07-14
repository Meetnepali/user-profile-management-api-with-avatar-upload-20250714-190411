# Guidance for Task

## Goal
Implement a secure, modular FastAPI API for authenticated user profile management, allowing users to update their display name, bio, and upload an avatar with proper validation and secure file handling.

### Key Requirements
- Complete the partially implemented codebase to ensure:
    - Endpoints for getting and updating profile details work with authentication.
    - Avatar upload only accepts JPEG/PNG files ≤ 2MB, using secure async file operations, and does **not** expose raw file paths.
    - SQLAlchemy is used for user profile persistence; all changes and queries require proper async session handling.
    - Pydantic is utilized for request/response validation and serialization.
    - Dependency injection is leveraged for authentication and DB session provision.
    - Clear, proper errors are returned for validation and storage failures (custom exception handlers).
    - No avatars are directly served from unprotected locations.
    - OpenAPI docs are customized for better developer experience.
    - Core tests are provided; make sure all required features and protections are covered so tests pass.

## What to Implement
- Complete any missing logic in endpoints, model relationships, or storage/data validation modules.
- Tighten file upload and validation logic to block disallowed types/sizes.
- Ensure all dependencies are correctly connected via FastAPI dependency injection.
- Wire up custom exception/error handling where indicated.
- Confirm database interactions follow async SQLAlchemy best practices.

## Constraints
- Do **not** expose unsafe paths or serve files directly.
- Code must be modular and readable: keep endpoints, models, schemas, auth, and storage logic cleanly separated.
- Use best practices for async file and DB operations.

## Verifying Your Solution
- Examine the provided automated tests in `app/tests/test_profile.py`. Ensure all tests pass:
    - User can update their own display name/bio via `PUT /profile`.
    - Avatar upload ONLY accepts valid JPEG/PNG up to 2MB, and saves the file securely, not exposing raw paths.
    - Disallowed avatar uploads are rejected with correct status codes and messages.
- Double-check OpenAPI output for clarity and correct schemas.

If all tests pass and manual checks for security and completeness succeed, your implementation is correct.
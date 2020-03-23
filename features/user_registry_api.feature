Feature: User Reistry API
    This should allow a user to be added, retrieved, updated, removed

    Scenario: Addding a new user
        Given a new user
        When posted to /user_registry_api/add_new_user
        Then a new record should be added to the Users table

    Scenario: Adding a new user without a required field
        Given a new user without a required field (e.g. name)
        When posted to /user_registry_api/add_new_user
        Then response from /user_registry_api/add_new_user should fail with "This field is required"

    Scenario: Adding a new user with numbers in name fields
        Given a new user with numbers in the name or surname fields
        When posted to /user_registry_api/add_new_user
        Then response from /user_registry_api/add_new_user should fail with "This field cannot contain numbers"

    Scenario: Adding a new user with an invalid email
        Given a new user with an invalid email
        When posted to /user_registry_api/add_new_user
        Then response from /user_registry_api/add_new_user should fail with "This field must contain a valid email address"

    Scenario: A user can be retrieved
        Given a new user posted to /user_registry_api/add_new_user
        When requested from /user_registry_api/get_user/<int:user_id>
        Then a user record should be retrieved

    Scenario: All users cas be retrieved with pagination
        Given 100 users posted to /user_registry_api/add_new_user
        When all users are requested from /user_registry_api/get_users
        Then 10 users per page should be retrieved

    Scenario: A user can be updated
        Given a new user posted to /user_registry_api/add_new_user
        When updated user data put to /user_registry_api/user/<int:user_id>
        Then the user record should be updated

    Scenario: A user can be deleted
        Given a new user posted to /user_registry_api/add_new_user
        When deleted using /user_registry_api/user/<int:user_id>
        Then the user record should be removed
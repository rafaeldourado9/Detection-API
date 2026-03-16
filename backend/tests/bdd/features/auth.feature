Feature: User Authentication
  As a user
  I want to register and login
  So that I can access the detection system

  Scenario: Register a new user
    Given I have valid registration data
    When I send a POST request to "/api/v1/auth/register"
    Then the response status code should be 201
    And the response should contain a user id

  Scenario: Login with valid credentials
    Given a registered user exists
    When I send a POST request to "/api/v1/auth/login" with valid credentials
    Then the response status code should be 200
    And the response should contain an access token

  Scenario: Login with invalid credentials
    Given a registered user exists
    When I send a POST request to "/api/v1/auth/login" with wrong password
    Then the response status code should be 401

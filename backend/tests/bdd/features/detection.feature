Feature: Object Detection
  As an authenticated user
  I want to submit images for detection
  So that I can get detected objects

  Scenario: Submit an image for detection
    Given I am an authenticated user
    When I upload an image to "/api/v1/detections"
    Then the response status code should be 202
    And the detection status should be "pending"

  Scenario: List my detections
    Given I am an authenticated user
    And I have submitted detections
    When I send a GET request to "/api/v1/detections"
    Then the response status code should be 200
    And I should see a list of detections

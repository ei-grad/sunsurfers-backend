Feature: Map
    In order to connect with sunsurfers nearby
    As an sunsurfer
    I want to see a map with sunsurfers who are in the area

    Scenario: Showing my location
        Given I allowed app to trace my location (standart function of the iOS/Android)
        When I open the map tab
        Then I see small circle with my location

    Scenario: Opening map. Separate sunsurfers found
        Given There are no two or more sunsurfers with overlay
        When I open the map tab
        Then I see circles with avatars with the radius 10 km nerby my location

    Scenario: Opening map. Separate sunsurfers found and overlaying users found
        Given There are two or more sunsurfers with overlay
        When I open the map tab
        Then I see circles with avatars with the radius 10 km
        And I see circle with the number of overlayed users

    Scenario: Changing the areas
        Given I am on the screen with the map
        When I zoom out map to another area
        Then I should see an updated map and users who are in the area

    Scenario: Zooming overlayed sunsurfers
        Given I see on the map the circle with the number of overlayed users
        When I zoom in the map
        Then I overlay disappears and I see separate circles with avatars 

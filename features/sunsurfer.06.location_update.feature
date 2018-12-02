Feature: Location update
    In order to show my place to other sunsurfers
    As an sunsurfer
    I want to choose update method (daily or when app is opened)

    Background:
        Given Previously I allowed to trace my location (standart function of the iOS/Android)

    Scenario: Automated update of the location
        Given I agree to update my location daily
        When new day is coming
        Then location and date should be updated

    Scenario: Update of the location when app is opening
        Given I disagree to update my location daily
        When I open the app
        Then location and date should be updated

    Scenario: Point in the home city
        Given I am in my home city
        When app update my location
        Then coordinates will be in the city center (not in my place)        

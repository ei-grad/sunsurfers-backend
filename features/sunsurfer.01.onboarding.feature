Feature: Onboarding
    In order to know the main benefits of the application
    As an sun surfer
    I want to see highlights of the core functionality 

    Scenario: I open the app
        Given I installed the app
        When I launch the app
        Then I see the the information about the functionality to search sunsurfers on the map
        And I see the the information about the functionality to quickly view profiles of sunsurfers who can host me
        And I see the the information about the functionality to connect with sunsurfers via Couchsurfing account
        And I see the the information about the functionality to connect with sunsurfers via Telegram
        And I see the the information about the functionality to connect with sunsurfers via Facebook
        And I see the the information about the functionality to connect with sunsurfers via VK

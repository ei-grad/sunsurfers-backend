Feature: filter the list of sunsurfers
  In order to find sunsurfer
	As an sun surfer
	I want to filter and search by various criteria 

	Background:
        Given I am on the tab list of sunsurfers

    Scenario: Opening the filter option
        When I click the filter icon 
        Then I see options to filter the whole list by one or many criteria: current location, isHost, participated events, occupation

    Scenario: Applying filter
    	When I choose one or many criteria
    	Then I see the filtered list
    	And I see chosen criteria

    Scenario: Reset filter
    	Given one or many criteria are applied
    	When I click the button "reset"
    	Then I see the whole list of sunsurfers without filtering

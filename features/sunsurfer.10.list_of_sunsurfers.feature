Feature: List of sunsurfers
  In order to connect with particular sunsurfer
	As an sun surfer
	I want to see a list with all sunsurfers

	Background:
        Given I am on the tab list of sunsurfers

    Scenario: Showing short summaries
        Then I see full list of the sunsurfers with pagination and the next fields: avatar, first name, occupation, isHost, bio
        And sorting is by Ascending by first name

    Scenario: Link to the full profile
    	When I click to the field name or occupation of the sunsurfer
    	Then I go to the full profile screen

    Scenario: Paginating through the list
    	When I click the number of pagination
    	Then I go the next part of the list with sunsurfers

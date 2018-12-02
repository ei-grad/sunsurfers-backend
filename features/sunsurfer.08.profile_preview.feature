Feature: profile preview
  In order to learn about sunsurfer who is nearby
	As an sunsurfer
	I want to see a short summary of his profile om the map

	Background:
        Given I am on the map tab

	Scenario: Showing short summary
        When I click to the circle with avatar
        Then I see short summary with the next fields: avatar, first_name, occupation, location_timestamp, bio, isHost and the button to the full proifle

	Scenario: Hiding short summary
		Given short summary is opened
		When I click outside the area of the short summary
		Then summary will hide and I see avatar of the user on the map 

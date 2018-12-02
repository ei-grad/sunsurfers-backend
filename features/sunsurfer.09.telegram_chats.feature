Feature: telegram chats
  In order to connect with the relavant sunsurfers based on certain topic
	As an sun surfer
	I want to see a list with the telegram chats that I can join

	Background:
        Given I am on the chat tab

	Scenario: Showing list with chats based on location
		Given I am on the tab with chat based on location
		Then I see chats grouped by country and all group are opened
		And I can hide chats inside group

	Scenario: opening the chat
		When I click on the name of the chat
		Then app suggest to open Telegram link

	Scenario: Switch list based on topic
        When I click to the another tab
        Then I see list base on another topic
*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${LOGIN_URL}  http://localhost:8002/user/login/
${BROWSER}  Chrome
${DELAY}  5s
${USERNAME}  sofiia@gmail.com
${PASSWORD}  sofiia_pass

*** Test Cases ***


User login create Post add Comment
    Open Browser  ${LOGIN_URL}  ${BROWSER}
    Set Window Size  1100  1000
    Input Text  name:username  ${USERNAME}
    Input Text  name:password  ${PASSWORD}
    Click Button  Sign up
    Wait Until Page Contains  Add Posts
    Page Should Contain  Add Posts
    Click Link  Add Posts
    Wait Until Page Contains Element  xpath://iframe
    Input Text  name:title  Sample title
    Select Frame  //iframe
    Click Element  xpath:/html/body/p
    Input Text  xpath:/html/body/p  Sample Description
    Unselect Frame
    Click Button  xpath://form/input[@type="submit"]
    Wait Until Location Is  http://localhost:8002/posts/
    Wait Until Page Contains  Sample title
    Page Should Contain  Sample Description
    Click Link  Read
    Wait Until Page Contains  Posts
    Input Text  id:id_text  Comment
    Click Element  xpath://form/input[@type="submit"]
    Click Link  Read
    Wait Until Page Contains  Comment
    [Teardown]  Close Browser

User Login, see posts and see post detail
    Open Browser  ${LOGIN_URL}  ${BROWSER}
    Input Text  name:username  ${USERNAME}
    Input Text  name:password  ${PASSWORD}
    Click Button  Sign up
    Wait Until Page Contains  ${USERNAME}
    Page Should Contain  ${USERNAME}
    Page Should Contain  Read
    Click Link  Read
    Wait Until Page Contains  Posts
    Page Should Contain  Posts
    [Teardown]  Close Browser

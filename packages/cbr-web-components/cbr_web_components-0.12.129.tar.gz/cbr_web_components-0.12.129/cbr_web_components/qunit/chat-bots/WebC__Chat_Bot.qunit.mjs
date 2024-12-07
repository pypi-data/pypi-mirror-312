import WebC__Target_Div                            from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../js/core/Web_Component.mjs'
import WebC__Chat_Bot                              from '../../js/chat-bot/WebC__Chat_Bot.mjs'
import { setup_mock_responses, set_mock_response } from '../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../js/cbr/CBR_Events.mjs";

const { module, test, only } = QUnit

const MOCK_CHAT_PATH = 'an/path/to/test-chat-123'
const MOCK_CHAT_SAVE_RESPONSE = { chat_path: MOCK_CHAT_PATH }

module('WebC__Chat_Bot', hooks => {
    let target_div
    let chat_bot

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        set_mock_response(`/api/user-data/chats/chat-add?chat_path=/${MOCK_CHAT_PATH}`, 'POST', MOCK_CHAT_SAVE_RESPONSE)

        target_div = WebC__Target_Div.add_to_body()
        chat_bot = await target_div.append_child(WebC__Chat_Bot)
        await chat_bot.wait_for__component_ready()
    })

    hooks.after(() => {
        chat_bot.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(chat_bot.tagName.toLowerCase()         , 'webc-chat-bot'        , 'Has correct tag name')
        assert.equal(chat_bot.constructor.element_name      , 'webc-chat-bot'        , 'Has correct element name')
        assert.equal(chat_bot.constructor.name              , 'WebC__Chat_Bot'       , 'Has correct class name')

        assert.ok(chat_bot.shadowRoot                                                , 'Has shadow root')
        assert.ok(chat_bot.data_chat_bot                                            , 'Has data chat bot instance')
        assert.equal(chat_bot.bot_name                     , 'ChatBot'              , 'Has default bot name')

        assert.ok(chat_bot instanceof Web_Component                                  , 'Extends Web_Component')
        assert.ok(chat_bot instanceof HTMLElement                                    , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = chat_bot.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                 , 'Has CSS rules')
        assert.ok(css_rules['.chatbot-ui']                                         , 'Has chatbot UI styles')
        assert.ok(css_rules['.chat-header']                                        , 'Has header styles')
        assert.ok(css_rules['.chat-messages']                                      , 'Has messages styles')
    })

    test('renders initial structure correctly', assert => {
        const container = chat_bot.query_selector('.chatbot-ui')
        assert.ok(container                                                         , 'Main container exists')

        const header = chat_bot.query_selector('.chat-header')
        assert.ok(header                                                            , 'Header exists')
        assert.ok(header.textContent.includes('ChatBot')                           , 'Shows bot name')

        const messages = chat_bot.query_selector('webc-chat-messages')
        assert.ok(messages                                                          , 'Messages component exists')

        const input = chat_bot.query_selector('webc-chat-input')
        assert.ok(input                                                             , 'Input component exists')

        const chat_ids = chat_bot.query_selector('#chat_ids')
        assert.ok(chat_ids                                                          , 'Chat IDs container exists')
    })

    test('handles maximize toggle', assert => {
        const container = chat_bot.query_selector('.chatbot-ui')
        const maximize_btn = chat_bot.query_selector('.maximize-button')

        assert.notOk(container.classList.contains('maximized')                      , 'Initially not maximized')

        maximize_btn.click()
        assert.ok(container.classList.contains('maximized')                         , 'Becomes maximized')

        maximize_btn.click()
        assert.notOk(container.classList.contains('maximized')                      , 'Becomes minimized')
    })

    test('handle_new_input_message - add a new message', async assert => {
        assert.expect(2)
        const test_message = { channel: chat_bot.channel, text: 'Test message' }
        const custom_event = new CustomEvent('-', { detail: test_message })
        assert.equal(chat_bot.messages.messages().length, 1)
        chat_bot.handle_new_input_message(custom_event)
        assert.equal(chat_bot.messages.messages().length, 2)
    })

    test('handles clear messages', assert => {
        const messages = chat_bot.query_selector('#chat_messages')
        const test_message = document.createElement('div')
        messages.appendChild(test_message)

        assert.ok(messages.childNodes.length > 0                                    , 'Has messages')
        const custom_event = new CustomEvent('-', {detail: { channel: chat_bot.channel }})
        chat_bot.handle_clear_messages(custom_event)
        assert.equal(messages.childNodes.length                 , 0                 , 'Messages cleared')

    })

    test('handles chat IDs update', async assert => {
        const chat_data = {
            channel        : chat_bot.channel,
            cbr_chat_id   : 'test-chat-123'
        }

        chat_bot.html_update_chat_ids_value(chat_data)
        const chat_ids = chat_bot.query_selector('#chat_ids')

        assert.ok(chat_ids.innerHTML.includes('/web/chat/view/test-chat-123')      , 'Shows chat link')
        assert.ok(chat_ids.innerHTML.includes('/web/chat/view/test-chat-123/pdf')  , 'Shows PDF link')
        assert.ok(chat_ids.innerHTML.includes('/web/chat/view/test-chat-123/image'), 'Shows image link')
    })

    test('handles save chat action', async assert => {
        const chat_data = { channel     : chat_bot.channel,  cbr_chat_id: MOCK_CHAT_PATH }

        chat_bot.html_update_chat_ids_value(chat_data)                                      // Setup chat IDs first

        const save_link = chat_bot.query_selector('#save-chat')
        assert.ok(save_link, 'Save link exists')

        save_link.click()
        const result = await chat_bot.wait_for_event(CBR_Events.CBR__CHAT__SAVED)
        assert.deepEqual(result, { channel:  chat_bot.channel,  saved_chat: { chat_path: MOCK_CHAT_PATH }})
        assert.equal(save_link.innerHTML                    , 'saved'              , 'Shows saved status')
        assert.equal(save_link.style.backgroundColor        , 'darkgreen'          , 'Shows success color')
    })

    test('handles save chat failure', async assert => {
        const bad_id = 'this/is/a/bad-id'
        set_mock_response('/api/user-data/chats/chat-add?chat_path=/test-chat-123', 'POST', { chat_path: bad_id })

        const chat_data = { channel     : chat_bot.channel,  cbr_chat_id: 'test-chat-123' }

        chat_bot.html_update_chat_ids_value(chat_data)
        const save_link = chat_bot.query_selector('#save-chat')
        save_link.click()
        const result = await chat_bot.wait_for_event(CBR_Events.CBR__CHAT__SAVE_ERROR)
        assert.deepEqual(result, { channel:  chat_bot.channel,  saved_chat: { chat_path: bad_id }})

        assert.ok(1)
        assert.equal(save_link.innerHTML                    , 'error'              , 'Shows error status')
        assert.equal(save_link.style.backgroundColor        , 'darkred'            , 'Shows error color')
    })

    test('visibility controls work', async assert => {
        chat_bot.hide()
        assert.ok(chat_bot.hidden                                                   , 'Can be hidden')

        chat_bot.show()
        assert.notOk(chat_bot.hidden                                               , 'Can be shown')
    })

    // test('handles edit mode attribute', assert => {
    //     chat_bot = WebC__Chat_Bot.create({ edit_mode: 'false' })
    //     assert.equal(chat_bot.edit_mode                    , 'false'               , 'Sets edit mode from attribute')
    //
    //     chat_bot = WebC__Chat_Bot.create()
    //     assert.equal(chat_bot.edit_mode                    , 'true'                , 'Uses default edit mode')
    // })
    //
    // test('handles show sent messages attribute', assert => {
    //     chat_bot = WebC__Chat_Bot.create({ show_sent_messages: 'false' })
    //     assert.equal(chat_bot.show_sent_messages           , 'false'               , 'Sets show sent from attribute')
    //
    //     chat_bot = WebC__Chat_Bot.create()
    //     assert.equal(chat_bot.show_sent_messages           , 'true'                , 'Uses default show sent')
    // })
})
import Chatbot_OpenAI   from '../../js/chat-bot/Chatbot_OpenAI.mjs'
import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__Target_Div from "../../js/utils/WebC__Target_Div.mjs";
import { Mock_Fetch,
         set_mock_response } from '../../js/testing/Mock_Fetch.mjs'

QUnit.module('Chatbot_OpenAI', function(hooks) {

    let chatbot_openai
    let target_div
    let div_system_prompt

    hooks.before(async (assert) => {
        assert.timeout(10)
        target_div                      = WebC__Target_Div.add_to_body().build({width: "50%"})
        chatbot_openai                  = target_div.append_child(Chatbot_OpenAI)
        await chatbot_openai.wait_for__component_ready()                                    // wait for the component to be ready
        div_system_prompt                 = document.createElement('div');                // todo: find a better way to add this temp DIV
        div_system_prompt.id              = 'system_prompt';
        div_system_prompt.style.display   = 'none';
        document.body.appendChild(div_system_prompt);
        assert.notEqual(chatbot_openai.messages, null)
        assert.equal(document.body.querySelector('#system_prompt').outerHTML, '<div id="system_prompt" style="display: none;"></div>')

    });

    hooks.beforeEach(() => {
        chatbot_openai.messages.messages_clear()
    })

    hooks.afterEach(() => {

    })

    hooks.after((assert) => {
        //assert.equal(chatbot_openai.messages.messages_size(),0)
        target_div.remove()
        div_system_prompt.remove()
    })

    QUnit.test('constructor', (assert) => {
        assert.ok(true)
        assert.ok(Chatbot_OpenAI.prototype instanceof Web_Component);
        assert.deepEqual(chatbot_openai.stop_fetch, false)
    })

    QUnit.test('add_thread_id_ui_link', (assert) => {
        assert.equal(chatbot_openai.messages.messages_size(),0)

        chatbot_openai.add_thread_id_ui_link()

        assert.equal(chatbot_openai.messages.messages_size(),1)
        let last_message = chatbot_openai.messages.messages()[0]
        let chat_thread_id = chatbot_openai.chat_thread_id
        let last_message_inner_html = `<a style="padding:0px" href="chat/view/${chat_thread_id}" target="_blank">view saved chat</a>`
        assert.deepEqual(last_message.innerHTML, last_message_inner_html)
    })

    QUnit.test('all_system_prompts', (assert) => {

        assert.deepEqual(chatbot_openai.all_system_prompts(), [])

        chatbot_openai.system_prompt = 'an system_prompt'
        assert.deepEqual(chatbot_openai.all_system_prompts(), ['an system_prompt'])

        chatbot_openai.system_prompt = null

        div_system_prompt.innerHTML = 'this is another system prompt'
        assert.deepEqual(chatbot_openai.all_system_prompts(), ['this is another system prompt'])
        div_system_prompt.innerHTML = ''
        assert.deepEqual(chatbot_openai.all_system_prompts(), [])
    })

    QUnit.test('apply_ui_tweaks', (assert) => {
        assert.deepEqual(chatbot_openai.all_system_prompts(), [])
        assert.equal(chatbot_openai.input.value   , '')
        assert.equal(chatbot_openai.initial_prompt, '')
        chatbot_openai.apply_ui_tweaks()
        assert.equal(chatbot_openai.input.value, '')

        chatbot_openai.initial_prompt = 'an initial prompt'
        chatbot_openai.apply_ui_tweaks()
        assert.equal(chatbot_openai.input.value, 'an initial prompt')

        chatbot_openai.initial_message = 'an initial message'
        chatbot_openai.apply_ui_tweaks()

        assert.deepEqual(chatbot_openai.messages.messages_size(),1)
        assert.deepEqual(chatbot_openai.messages.messages()[0].outerHTML, '<webc-chat-message type="initial">an initial message</webc-chat-message>')

        chatbot_openai.messages.messages_clear()
        chatbot_openai.initial_message = null

        // chatbot_openai.system_prompt = 'an system prompt'
        // chatbot_openai.apply_ui_tweaks()
        // assert.deepEqual(chatbot_openai.messages.messages_size(),1)
        // assert.deepEqual(chatbot_openai.messages.messages()[0].outerHTML, '<webc-chat-message type="system" style="display: inherit;">an system prompt</webc-chat-message>')

        chatbot_openai.messages.messages_clear()
    })



    QUnit.test('post_openai_prompt_with_stream', async (assert) => {

        const fake_fetch_request_post = async (url, body) => {
            return {
                ok      : true    ,
                status  : 200     ,
                body    : { getReader() { return { read() {return Promise.resolve({ done: true,
                                                                                    value: new TextEncoder().encode('{"message": "fake data"}' )})}}}}
            };
        }
        chatbot_openai.fetch_request_post = fake_fetch_request_post

        const done          = assert.async();

        const end_test = () => {
            chatbot_openai.messages.messages_clear()
            done()
        }

        const user_prompt = '2+2'
        const images      = null

        chatbot_openai.addEventListener('streamComplete', function(event) {
            assert.deepEqual(event.detail, null)
            end_test();
            }, { once: true });

        chatbot_openai.post_openai_prompt_with_stream(user_prompt, images)

    });



    // QUnit.test('handles stream responses correctly', async assert => {
    //     //const done = assert.async()
    //     assert.expect(3)
    //
    //     const chunks = ['Hello', ' World', '!']
    //     const mock_fetch = Mock_Fetch.apply_mock(chatbot_openai)
    //     mock_fetch.set_stream_response(chatbot_openai.url, chunks)
    //
    //     chatbot_openai.addEventListener('streamData', (event) => {
    //         assert.ok(event.detail.data, 'Receives stream chunk')
    //     })
    //
    //     chatbot_openai.addEventListener('streamComplete', () => {
    //         assert.ok(true, 'Stream completes successfully')
    //         done()
    //     })
    //
    //     await chatbot_openai.post_openai_prompt_with_stream('test prompt', [])
    // })
    //
    // QUnit.test('calculates chat histories correctly', async assert => {
    //     // Add messages in the way the project does it
    //     chatbot_openai.messages.add_message_sent('Question 1').message('Question 1')
    //     chatbot_openai.messages.add_message_received('Answer 1').message('Answer 1')
    //     chatbot_openai.messages.add_message_sent('Question 2').message('Question 2')
    //
    //     const histories = chatbot_openai.calculate_histories()
    //
    //     assert.equal(histories.length, 1, 'Captures complete Q&A pairs')
    //     assert.deepEqual(histories[0], {
    //         question: 'Question 1',
    //         answer: 'Answer 1'
    //     }, 'History pair matches expected format')
    // })
    //
    // QUnit.test('handles model selection', async assert => {
    //     const model_event = new CustomEvent('select_model', {
    //         detail: {
    //             platform: 'test_platform',
    //             provider: 'test_provider',
    //             model: 'test_model',
    //             channel: chatbot_openai.channel
    //         }
    //     })
    //
    //     await chatbot_openai.on_select_model(model_event)
    //
    //     assert.equal(chatbot_openai.platform, 'test_platform', 'Updates platform')
    //     assert.equal(chatbot_openai.provider, 'test_provider', 'Updates provider')
    //     assert.equal(chatbot_openai.model, 'test_model', 'Updates model')
    // })
    //
    // QUnit.test('handles stream stopping', async assert => {
    //     assert.expect(2)
    //     const done = assert.async()
    //
    //     chatbot_openai.stop_fetch = false
    //     assert.notOk(chatbot_openai.stop_fetch, 'Stop flag starts false')
    //
    //     const stop_event = new CustomEvent('stop_stream', {
    //         detail: { channel: chatbot_openai.channel }
    //     })
    //
    //     await chatbot_openai.on_stop_stream(stop_event)
    //     assert.ok(chatbot_openai.stop_fetch, 'Sets stop flag to true')
    //     done()
    // })
    //
    // QUnit.test('handles message sending with targets', async assert => {
    //     assert.expect(2)
    //     const done = assert.async()
    //
    //     chatbot_openai.target = 'specific_target'
    //     chatbot_openai.fetch = false  // Prevent actual API calls
    //
    //     // Different target - should be ignored
    //     await chatbot_openai.on_message_sent({
    //         detail: {
    //             target: 'different_target',
    //             message: { user_prompt: 'test' }
    //         }
    //     })
    //     assert.ok(true, 'Ignores non-matching target')
    //
    //     // Matching target
    //     chatbot_openai.target = 'matching_target'
    //     await chatbot_openai.on_message_sent({
    //         detail: {
    //             target: 'matching_target',
    //             message: { user_prompt: 'test' }
    //         }
    //     })
    //     assert.ok(true, 'Processes matching target')
    //     done()
    // })
    //
    // QUnit.test('handles non-streamed responses', async assert => {
    //     assert.expect(2)
    //     const done = assert.async()
    //
    //     set_mock_response(chatbot_openai.url, 'POST', {
    //         success: true,
    //         data: { message: 'Test response' }
    //     })
    //
    //     chatbot_openai.stream = false
    //
    //     chatbot_openai.addEventListener('streamData', (event) => {
    //         assert.ok(event.detail.data, 'Receives response data')
    //     })
    //
    //     chatbot_openai.addEventListener('streamComplete', () => {
    //         assert.ok(true, 'Completes non-streamed response')
    //         done()
    //     })
    //
    //     await chatbot_openai.post_openai_prompt_with_stream('test prompt', [])
    // })
})
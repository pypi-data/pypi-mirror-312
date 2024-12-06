import Web_Component       from "../core/Web_Component.mjs"        ;
import Data__Chat_Bot      from "../data/Data__Chat_Bot.mjs" ;
import WebC__Chat_Input    from "./WebC__Chat_Input.mjs"     ;
import WebC__Chat_Messages from "./WebC__Chat_Messages.mjs"  ;
import CSS__WebC__Chat_Bot from "./CSS__WebC__Chat_Bot.mjs"  ;
import A                   from "../core/A.mjs"              ;
import Div                 from "../core/Div.mjs"            ;
import Text                from "../core/Text.mjs"           ;
import Tag                 from "../core/Tag.mjs"            ;
import Icon__Mappings      from "../css/icons/Icon__Mappings.mjs";
import Icon                from "../css/icons/Icon.mjs";

export default class WebC__Chat_Bot extends Web_Component {

    static url_current_user_add_chat_id = '/api/user-data/chats/chat-add?chat_path='

    constructor() {
        super();
        this.is_maximized       = false;
        this.target_element     = null
        this.data_chat_bot      = new Data__Chat_Bot()
        this.bot_name           = 'ChatBot'
        this.channels.push('WebC__Chat_Bot')

    }

    // properties

    get chat_ids() {
        return this.query_selector('#chat_ids')
    }

    get input() {
        return this.query_selector('#chat_input').input
    }

    get messages() {
        return this.query_selector('#chat_messages')        //todo: refactor chat_messages
    }

    get save_chat_link() {
        return this.query_selector('#save-chat')
    }

    get target_element_style() {
        return this.target_element?.style
    }

    get target_element_style_computed() {
        return getComputedStyle(this.target_element)
    }

    // Web_Component overrider methods

    async apply_css() {
        new CSS__WebC__Chat_Bot(this).apply_framework()
    }

    load_attributes() {
        super.load_attributes();
        this.show_sent_messages = this.getAttribute('show_sent_messages') || false

        if (this.getAttribute('edit_mode')  === null) {
            this.edit_mode = 'true' }
        else {
            this.edit_mode = this.getAttribute('edit_mode')
        }

        if (this.getAttribute('show_sent_messages')  === null) {
            this.show_sent_messages = 'true' }
        else {
            this.show_sent_messages = this.getAttribute('show_sent_messages')
        }
    }

    add_event_listeners() {
        window.addEventListener('new_input_message', (e)=>{ this.handle_new_input_message(e.detail) });
        window.addEventListener('clear_messages'   , (e)=>{ this.handle_clear_messages   (e.detail) })
        window.addEventListener('new_chat_ids'     , (e)=>{ this.handle_new_chat_ids     (e.detail) })
        this.add_event_listener('.maximize-button', 'click', () => this.toggle_maximize())
    }

    html() {
        return this.div_chatbot_ui()
    }


    // instance methods
    handle_new_input_message(event_data) {
        if (event_data?.channel === this.channel) {
            this.messages.add_message_sent(event_data) }
        if (this.channel?.startsWith('shared-llm')) {
            this.messages.add_message_sent(event_data) }

    }
    handle_clear_messages(event_data) {
        if (event_data?.channel === this.channel) {
            this.clear_messages()
        }
    }
    handle_new_chat_ids(event_data) {
        if (event_data?.channel === this.channel) {
            this.html_update_chat_ids_value(event_data)
        }
    }
    clear_messages() {
        $(this.messages.childNodes).remove()
    }



    create_header() {
        const tag = new Tag()
        const div_chat_header = tag.clone({tag: 'div', class: 'chat-header'})
        const header_content  = new Div ({ class: 'header-content' })
        const header_text     = new Text({ class: 'chat-header-title', value: this.bot_name })
        const maximize_btn    = new Div ({class: 'maximize-button'                 })
        const maximize_icon   = new Icon({class: 'maximize-icon' , icon: 'maximize', })
        maximize_btn.add_element(maximize_icon)

        header_content .add_elements(header_text, maximize_btn)
        div_chat_header.add(header_content)

        return div_chat_header
    }

    //todo : refactor this to use use add_web_components (and double check if we still need this class)
    div_chatbot_ui() {

        const tag = new Tag()
        const tag_chat_messages = WebC__Chat_Messages.element_name
        const tag_chat_input    = WebC__Chat_Input   .element_name
        const chat_messages__id = 'chat_messages'
        const chat_input__id    = 'chat_input'

        tag.html_config.include_id=false

        const div_chatbot_ui     = tag.clone({tag:'div'            , class:'chatbot-ui'                           })
        const div_chat_ids       = new Tag  ({tag:'div'            , class:'chat-ids'     , id: 'chat_ids'        })
        const webc_chat_messages = new Tag  ({tag:tag_chat_messages, class:'chat-messages', id: chat_messages__id })
        const webc_chat_input    = new Tag  ({tag:tag_chat_input   , class:'chat-input-ui', id: chat_input__id    })

        webc_chat_input   .attributes.channel            = this.channel
        webc_chat_messages.attributes.channel            = this.channel
        webc_chat_messages.attributes.show_sent_messages = this.show_sent_messages
        webc_chat_messages.attributes.edit_mode          = this.edit_mode

        div_chatbot_ui.add(this.create_header())
        div_chatbot_ui.add(div_chat_ids     )
        div_chatbot_ui.add(webc_chat_messages)
        div_chatbot_ui.add(webc_chat_input)

        div_chatbot_ui  .html_config.trim_final_html_code = true
        div_chat_ids.value ='...'
        return div_chatbot_ui
    }

    html_update_chat_ids_value(event_data) {
        if (!event_data) {
            return
        }
        if (event_data?.cbr_chat_id === '') {
            return
        }

        const cbr_chat_id        = event_data?.cbr_chat_id          || ''
        //const cbr_chat_thread_id = event_data?.cbr_chat_thread_id   || ''
        const link__chat         = `/web/chat/view/${cbr_chat_id}`
        const link__chat_pdf     = `${link__chat}/pdf`
        const link__chat_image   = `${link__chat}/image`

        //const link__thread       = `chat/view/${cbr_chat_thread_id}`

        const div_chat_ids = new Div()
        const text_pipe     = new Text({value: '|'})
        const a_save        = new A   ({value: 'save'       , attributes: { href: '#'              , id:'save-chat' , class:'save-chat'}})
        const a_chat        = new A   ({value: 'share chat' , attributes: { href: link__chat       , target:'_blank'}})
        const a_chat_pdf    = new A   ({value: 'share pdf'  , attributes: { href: link__chat_pdf   , target:'_blank'}})
        const a_chat_image  = new A   ({value: 'share image', attributes: { href: link__chat_image , target:'_blank'}})

        div_chat_ids.add_elements( a_save, text_pipe, a_chat, text_pipe, a_chat_pdf, text_pipe, a_chat_image)
        this.chat_ids.innerHTML = div_chat_ids.html()

        this.save_chat_link.addEventListener('click'         , async (event) => this.on_save_chat_click(event, cbr_chat_id))
    }


    hide() {
        this.hidden = true
        return this
    }

    set_input_value(value)  {
        let event_data = {'value': value }
        this.events_utils.events_dispatch.send_to_channel('set_value', this.channel, event_data)
    }


    show() {
        this.hidden = false
        return this
    }

    async on_save_chat_click(event, cbr_chat_id) {
        event.preventDefault()
        const url = WebC__Chat_Bot.url_current_user_add_chat_id + cbr_chat_id
        const response = await fetch(url, { method : 'POST'});
        const saved_chat = await response.json()
        if (saved_chat.chat_path === cbr_chat_id) {
            this.save_chat_link.innerHTML = 'saved'
            this.save_chat_link.style.backgroundColor = 'DarkGreen'
            this.save_chat_link.style.fontWeight      = '100'
        }
        else {
            this.save_chat_link.style.backgroundColor = 'DarkRed'
            this.save_chat_link.style.fontWeight      = '100'
            this.save_chat_link.innerHTML             = 'error'
        }
    }

    // Maximize button section

    toggle_maximize() {
        this.is_maximized = !this.is_maximized;
        const container   = this.query_selector('.chatbot-ui');
        const btn         = this.query_selector('.maximize-button');
        const icon        = btn.querySelector('.maximize-icon');

        if (this.is_maximized) {
            container.classList.add('maximized');
            icon.textContent = Icon__Mappings.getIcon('minimize');
        } else {
            container.classList.remove('maximized');
            icon.textContent = Icon__Mappings.getIcon('maximize');
        }
    }
}

WebC__Chat_Bot.define()


// todo: add this code to a separate class that provides a floating chat bot
    // in constructor
        //
        //      this.is_resizing        = false;
        //      this.is_dragging        = false;
        //      this.drag_offset        = { x: 0, y: 0 };
        //      this.current_dims       = { width: 0, height: 0 };
        //      this.resize_edge        = null;

        // in add_event_hooks()

        // // move chat ui via header
        // const header = this.query_selector('.chat-header');
        // header.addEventListener('mousedown', (e) => this.start_drag(e));
        // document.addEventListener('mousemove', (e) => this.handle_drag(e));
        // document.addEventListener('mouseup', () => this.stop_drag());
        // // resize chat ui via edges
        // // Add resize handles
        // const container = this.query_selector('.chatbot-ui');
        // const handles = this.create_resize_handles();
        // handles.forEach(handle => {
        //     //console.log('handle', handle.dom_create())
        //     const dom_element = handle.dom_create()
        //     container.appendChild(dom_element);
        //     // container.appendChild(handle.dom_element());
        //     //
        //     const edge = handle.class.split('resize-')[2];
        //
        //     dom_element.addEventListener('mousedown', (e) => {
        //         e.stopPropagation();
        //         this.start_resize(e, edge);
        //     });
        // });
        //
        // // Add resize event listeners
        // document.addEventListener('mousemove', (e) => {
        //     if (this.is_resizing) {
        //         this.handle_resize(e);
        //     }
        // });
        //
        // document.addEventListener('mouseup', () => {
        //     this.stop_resize();
        // });
    // toggle_maximize() {
    //     if (this.is_resizing) return;
    //     this.is_maximized = !this.is_maximized;
    //     const container   = this.query_selector('.chatbot-ui');
    //     const btn         = this.query_selector('.maximize-button');
    //     const icon        = btn.querySelector('.maximize-icon');
    //
    //     if (this.is_maximized) {
    //         // container.style.width  = 'calc(100vw - 100px)';
    //         // container.style.height = 'calc(100vh - 100px)';
    //         // container.style.right  = '50px';
    //         // container.style.bottom = '50px';
    //         icon.textContent = Icon__Mappings.getIcon('minimize');
    //         container.classList.add('maximized');
    //         // container.style.position = 'fixed';
    //         // container.style.left     = "50px"
    //         // container.style.right    = "50px"
    //         // container.style.top      = "50px"
    //         // container.style.bottom   = "50px"
    //     } else {
    //         icon.textContent = Icon__Mappings.getIcon('maximize');
    //         container.classList.remove('maximized');
    //         // container.style.width  = `${this.current_dims.width}px`;
    //         // container.style.height = `${this.current_dims.height}px`;
    //         // container.style.right  = 'auto';
    //         // container.style.bottom = 'auto';
    //         container.style.position = 'absolute';
    //         container.style.left     = 0
    //         container.style.right    = 0
    //         container.style.top      = 0
    //         container.style.bottom   = 0
    //
    //     }
    // }

    // // chat ui drag via header
    // start_drag(e) {
    //     if (!e.target.closest('.chat-header')) { return }
    //
    //     this.is_dragging = true;
    //     const container  = this.query_selector('.chatbot-ui');
    //     const rect       = container.getBoundingClientRect();
    //
    //
    //     this.current_dims = { width : rect.width,                           // Store current dimensions before starting drag
    //                           height: rect.height };
    //
    //     this.drag_offset  = {x: e.clientX - rect.left,
    //                          y: e.clientY - rect.top };
    //
    //
    //     if (!this.is_maximized) {                                           // Set initial position and dimensions
    //         container.style.width  = `${this.current_dims.width}px`;
    //         container.style.height = `${this.current_dims.height}px`;
    //     }
    //
    //     container.classList.add('dragging');
    // }
    //
    // handle_drag(e) {
    //     if (!this.is_dragging) { return }
    //
    //     const container = this.query_selector('.chatbot-ui');
    //     const new_x = e.clientX - this.drag_offset.x;
    //     const new_y = e.clientY - this.drag_offset.y;
    //
    //     // Apply different positioning based on state
    //     if (this.is_maximized) {
    //         // When maximized, maintain the expanded size but allow repositioning
    //         container.style.left   = `${new_x}px`;
    //         container.style.right  = 'auto';
    //         container.style.top    = `${new_y}px`;
    //         container.style.bottom = 'auto';
    //         container.style.width  = 'calc(100vw - 100px)';  // Maintain maximized width
    //         container.style.height = 'calc(100vh - 100px)';  // Maintain maximized height
    //     } else {
    //         // When minimized, maintain original dimensions
    //         container.style.position = 'fixed';
    //         container.style.left     = `${new_x}px`;
    //         container.style.top      = `${new_y}px`;
    //         container.style.width    = `${this.current_dims.width}px`;
    //         container.style.height   = `${this.current_dims.height}px`;
    //     }
    // }
    //
    // stop_drag() {
    //     if (!this.is_dragging) { return }
    //
    //     this.is_dragging = false;
    //     const container = this.query_selector('.chatbot-ui');
    //     container.classList.remove('dragging');
    // }
    //
    // // resize chat ui via edges
    //
    // create_resize_handles() {
    //     const edges = [
    //         'top-left', 'top-right', 'bottom-left', 'bottom-right',
    //         'top', 'bottom', 'left', 'right'
    //     ];
    //
    //     return edges.map(edge => {
    //         const handle = new Div({
    //             class: `resize-handle resize-${edge}`
    //         });
    //         return handle;
    //     });
    // }
    //
    // start_resize(e, edge) {
    //     if (this.is_maximized) return;
    //
    //     this.is_resizing = true;
    //     this.resize_edge = edge;
    //
    //     const container = this.query_selector('.chatbot-ui');
    //     const rect = container.getBoundingClientRect();
    //
    //     this.current_dims = {
    //         width: rect.width,
    //         height: rect.height,
    //         x: rect.left,
    //         y: rect.top
    //     };
    //
    //     this.resize_start = {
    //         x: e.clientX,
    //         y: e.clientY
    //     };
    //
    //     container.classList.add('resizing');
    // }
    //
    // handle_resize(e) {
    //
    //     console.log('starting resize', this.resize_edge)
    //     if (!this.is_resizing) return;
    //
    //     const container = this.query_selector('.chatbot-ui');
    //     const dx = e.clientX - this.resize_start.x;
    //     const dy = e.clientY - this.resize_start.y;
    //
    //     let new_width  = this.current_dims.width;
    //     let new_height = this.current_dims.height;
    //     let new_x      = this.current_dims.x;
    //     let new_y      = this.current_dims.y;
    //
    //     // Handle different resize edges
    //     switch (this.resize_edge) {
    //         case 'right':
    //         case 'bottom-right':
    //         case 'top-right':
    //             new_width = Math.max(300, this.current_dims.width + dx);
    //             break;
    //         case 'left':
    //         case 'bottom-left':
    //         case 'top-left':
    //             const width_diff = Math.max(300 - this.current_dims.width, + dx);
    //             new_width = this.current_dims.width - width_diff;
    //             new_x     = this.current_dims.x + width_diff;
    //             break;
    //     }
    //
    //
    //     switch (this.resize_edge) {
    //         case 'bottom':
    //         case 'bottom-left':
    //         case 'bottom-right':
    //             new_height = Math.max(350, this.current_dims.height + dy);
    //             break;
    //         case 'top':
    //         case 'top-left':
    //         case 'top-right':
    //             const height_diff = Math.max(350 - this.current_dims.height, + dy);
    //             new_height = this.current_dims.height - height_diff;
    //             new_y = this.current_dims.y + height_diff;
    //             break;
    //     }
    //
    //     // Apply new dimensions
    //     container.style.width = `${new_width}px`;
    //     container.style.height = `${new_height}px`;
    //     container.style.left = `${new_x}px`;
    //     container.style.top = `${new_y}px`;
    // }
    //
    // stop_resize() {
    //     if (!this.is_resizing) return;
    //
    //     this.is_resizing = false;
    //     this.resize_edge = null;
    //
    //     const container = this.query_selector('.chatbot-ui');
    //     container.classList.remove('resizing');
    //
    //     // Update current dimensions
    //     const rect = container.getBoundingClientRect();
    //     this.current_dims = {
    //         width: rect.width,
    //         height: rect.height
    //     };
    // }
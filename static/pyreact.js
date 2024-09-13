class Pyreact {
    constructor() {
        this.state = window.INITIAL_STATE || {};
        this.components = {};
        this.eventListeners = {};
        this.observer = new MutationObserver(this.handleMutations.bind(this));
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeComponents();
            this.setupRouting();
            this.setupWebSocket();
            this.observeDOM();
        });
    }

    initializeComponents() {
        const componentElements = document.querySelectorAll('[data-pyreact-component]');
        componentElements?.forEach(element => {
            const componentName = element?.getAttribute('data-pyreact-component');
            this.initializeComponent(componentName, element);
        });
        this.loadCustomComponents();
    }
    retriggerCSS() {
        const links = document.querySelectorAll('link[rel="stylesheet"], style');
        links.forEach(link => {
          if (link.tagName === 'LINK') {
            const clonedLink = link.cloneNode();
            clonedLink.href += '?v=' + Date.now(); // Append a cache-busting query parameter
            link.parentNode.replaceChild(clonedLink, link);
          } else if (link.tagName === 'STYLE') {
            const clonedStyle = document.createElement('style');
            clonedStyle.textContent = link.textContent;
            link.parentNode.replaceChild(clonedStyle, link);
          }
        });
      }
    
    

    loadCustomComponents() {
        const componentTags = document.querySelectorAll('component');
        componentTags.forEach(async (tag) => {
            const link = tag.getAttribute('data-link');
            const props = JSON.parse(tag.getAttribute('data-props') || '{}');
            const componentHtml = await this.loadComponent(link, props);
            
            tag.innerHTML = componentHtml;
                    this.retriggerCSS();
        
            this.setupComponentEventListeners(tag);
        });
    }

    initializeComponent(name, element) {
        if (!this.components[name]) {
            this.components[name] = {
                elements: [element],
                state: this.state[name] || {},
                id: element?.getAttribute('data-component-id')
            };
        } else {
            this.components[name].elements.push(element);
        }
        this.setupComponentEventListeners(element);
    }

    setupComponentEventListeners(element) {
        const events = ['click', 'input', 'change', 'submit'];
        events.forEach(eventType => {
            element.querySelectorAll(`[data-event="${eventType}"]`)?.forEach(el => {
                const handlerName = el?.getAttribute(`data-${eventType}-handler`);
                if (handlerName) {
                    el.addEventListener(eventType, async (event) => {
                        event.preventDefault();
                        await this.triggerEvent(handlerName, event);
                    });
                }
            });
        });
    }

    observeDOM() {
        const config = { attributes: true, childList: true, subtree: true };
        this.observer.observe(document.body, config);
    }

    handleMutations(mutations) {
        mutations.forEach(mutation => {
            if (mutation.type === 'attributes') {
                this.handleAttributeChange(mutation.target, mutation.attributeName);
            } else if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        this.setupComponentEventListeners(node);
                        if (node.tagName.toLowerCase() === 'component') {
                            this.loadCustomComponents();
                        }
                    }
                });
            }
        });
    }

    handleAttributeChange(element, attributeName) {
        if (element.tagName.toLowerCase() === 'component' && 
            (attributeName === 'data-link' || attributeName === 'data-props')) {
            this.loadCustomComponents();
        } else if (attributeName.startsWith('data-event-')) {
            const eventType = attributeName.replace('data-event-', '');
            const handlerName = element.getAttribute(`data-${eventType}-handler`);
            if (handlerName) {
                element.addEventListener(eventType, async (event) => {
                    event.preventDefault();
                    await this.triggerEvent(handlerName, event);
                });
            }
        }
    }

    async updateComponents() {
        for (const componentName of Object.keys(this.components)) {
            await this.updateComponent(componentName);
        }
    }

    async updateComponent(name) {
        try {
            const response = await this.getFromServer(`/api/component/${name}`);
            if (!response) return;

            const newHtml = response;
            const elements = document.querySelectorAll(`[data-pyreact-component="${name}"]`);
            elements?.forEach(el => {
                el.innerHTML = newHtml;
                this.initializeComponent(name, el);
            });
        } catch (error) {
            console.error('Update error:', error);
        }
    }

    setupRouting() {
        document.body.addEventListener('click', (e) => {
            const link = e.target.closest('[data-pyreact-link]');
            if (link && link.getAttribute('href').startsWith('/')) {
                e.preventDefault();
                this.navigate(link.href);
            }
        });

        window.addEventListener('popstate', () => {
            this.updateContent(window.location.pathname);
        });
    }

    async navigate(url) {
        history.pushState(null, '', url);
        await this.updateContent(url);
    }

    async updateContent(url) {
        try {
            if (document.startViewTransition) {
                document.startViewTransition(async () => {
                    const response = await fetch(url);
                    const html = await response.text();
                    const contentElement = document.getElementById('root');
                    contentElement.innerHTML = html;
                    this.initializeComponents();
                });
            } else {
                const response = await fetch(url);
                const html = await response.text();
                const contentElement = document.getElementById('root');
                contentElement.innerHTML = html;
                this.initializeComponents();
            }
        } catch (error) {
            console.error('Navigation error:', error);
        }
    }

    async triggerEvent(eventName, ...args) {
        try {
            const result = await this.postToServer('/api/event', {
                event_name: eventName,
                args: args,
                component_id: this.getComponentId(args)
            });
            
            if (result.newState) {
                this.state = result.newState;
                await this.updateComponents();
            }

            if (result.html) {
                const componentId = this.getComponentId(args);
                const componentElement = document.querySelector(`[data-component-id="${componentId}"]`);
                if (componentElement) {
                    componentElement.innerHTML = result.html;
                    this.initializeComponent(componentElement.getAttribute('data-pyreact-component'), componentElement);
                }
            } else if (result.error) {
                console.error('Event error:', result.error);
            }

            return result;
        } catch (error) {
            console.error('Event trigger error:', error);
        }
    }

    getComponentId(args) {
        if (args.length > 0 && args[0] instanceof Event) {
            return args[0].target.closest('[data-component-id]')?.getAttribute('data-component-id');
        }
        return null;
    }

    async getFromServer(url) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.text();
    }

    async postToServer(url, data, expectedResponseType = 'json') {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        switch (expectedResponseType.toLowerCase()) {
            case 'json':
                return await response.json();
            case 'text':
                return await response.text();
            case 'arraybuffer':
                return await response.arrayBuffer();
            case 'blob':
                return await response.blob();
            default:
                return response;
        }
    }

    async loadComponent(link, props) {
        try {
            const response = await this.postToServer('/api/load-component', {
                component_name: link,
                props: props
            }, 'text');
            return response;
        } catch (error) {
            console.error('Error loading component:', error);
            return '<p>Error loading component</p>';
        }
    }

    setupWebSocket() {
        if (window.location.protocol === 'http:') {
            const ws = new WebSocket(`ws://${window.location.host}/ws`);
            ws.onmessage = (event) => {
                if (event.data === 'reload') {
                    this.reloadPage();
                }
            };
        }
    }

    reloadPage() {
        const currentTimestamp = new Date().getTime();
        const scripts = document.getElementsByTagName('script');
        const links = document.getElementsByTagName('link');

        for (let i = 0; i < scripts.length; i++) {
            const src = scripts[i].getAttribute('src');
            if (src) {
                scripts[i].setAttribute('src', this.updateQueryStringParameter(src, 'v', currentTimestamp));
            }
        }

        for (let i = 0; i < links.length; i++) {
            const href = links[i].getAttribute('href');
            if (href && links[i].rel === 'stylesheet') {
                links[i].setAttribute('href', this.updateQueryStringParameter(href, 'v', currentTimestamp));
            }
        }

        window.location.reload();
    }

    updateQueryStringParameter(uri, key, value) {
        const re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
        const separator = uri.indexOf('?') !== -1 ? "&" : "?";
        if (uri.match(re)) {
            return uri.replace(re, '$1' + key + "=" + value + '$2');
        } else {
            return uri + separator + key + "=" + value;
        }
    }
}

const pyreact = new Pyreact();
window.pyreact = pyreact;
import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './ClientDashboard.css'
import './LandingPage.css'

const SUGGESTED_PROMPTS = [
    'I have a tenant rights dispute',
    'I need help with an employment issue',
    'Property ownership conflict',
    'Consumer complaint against a company',
    'Divorce and custody matter',
    'Cybercrime or online fraud',
]

const PAST_SESSIONS = [
    { id: 1, title: 'Tenant Eviction Notice Query', date: 'Today' },
    { id: 2, title: 'Employment Termination Rights', date: 'Yesterday' },
    { id: 3, title: 'Property Boundary Dispute', date: 'Last 7 days' },
]

function generateAIResponse(query) {
    const lowerQuery = query.toLowerCase()

    let area = 'General Civil Law'
    let analysis = ''
    let steps = []

    if (lowerQuery.includes('tenant') || lowerQuery.includes('rent') || lowerQuery.includes('landlord') || lowerQuery.includes('evict')) {
        area = 'Tenancy & Property Law'
        analysis = 'Based on your description, this appears to involve tenant rights under the applicable Rent Control Act. Tenants are generally protected against arbitrary eviction and have the right to a fair hearing before any eviction order. Your landlord must follow the due legal process.'
        steps = [
            'Gather your lease agreement and all communication records',
            'Document any notices received with dates',
            'File a complaint with the Rent Control Authority if needed',
            'Consider mediation before litigation',
        ]
    } else if (lowerQuery.includes('employ') || lowerQuery.includes('job') || lowerQuery.includes('fired') || lowerQuery.includes('termination') || lowerQuery.includes('salary')) {
        area = 'Employment & Labour Law'
        analysis = 'Your query relates to employment rights. Under labour laws, employees are entitled to proper notice periods, fair termination procedures, and outstanding dues. Wrongful termination can be challenged through the Labour Court or appropriate tribunal.'
        steps = [
            'Collect your employment contract and payslips',
            'Document the termination communication',
            'File a grievance with the Labour Commissioner',
            'Explore conciliation proceedings',
        ]
    } else if (lowerQuery.includes('property') || lowerQuery.includes('land') || lowerQuery.includes('ownership') || lowerQuery.includes('boundary')) {
        area = 'Property & Real Estate Law'
        analysis = 'Property disputes require careful examination of title deeds, registration documents, and possession history. The Transfer of Property Act and Registration Act govern these matters. It is important to establish clear title and chain of ownership.'
        steps = [
            'Obtain certified copies of all property documents',
            'Verify the title through the Sub-Registrar office',
            'Get a survey and demarcation done if boundary is disputed',
            'Explore settlement before filing a civil suit',
        ]
    } else if (lowerQuery.includes('divorce') || lowerQuery.includes('custody') || lowerQuery.includes('marriage') || lowerQuery.includes('alimony')) {
        area = 'Family Law'
        analysis = 'Family matters including divorce and custody are handled under personal laws and the Family Courts Act. The court prioritizes the welfare of children in custody matters and considers various factors for maintenance and alimony.'
        steps = [
            'Gather marriage certificate and relevant documents',
            'Document any instances relevant to your case',
            'Consider mediation through Family Court counsellors',
            'File a petition in the Family Court',
        ]
    } else if (lowerQuery.includes('cyber') || lowerQuery.includes('fraud') || lowerQuery.includes('online') || lowerQuery.includes('scam') || lowerQuery.includes('hack')) {
        area = 'Cyber Crime & IT Law'
        analysis = 'Cyber crimes fall under the Information Technology Act, 2000. This includes online fraud, identity theft, hacking, and data breaches. Quick action is essential to preserve digital evidence and increase the chances of recovery.'
        steps = [
            'Preserve all digital evidence (screenshots, emails, URLs)',
            'File a complaint on the National Cyber Crime Portal',
            'Lodge an FIR at the nearest Cyber Crime police station',
            'Contact your bank immediately if financial fraud is involved',
        ]
    } else if (lowerQuery.includes('consumer') || lowerQuery.includes('complaint') || lowerQuery.includes('product') || lowerQuery.includes('defective')) {
        area = 'Consumer Protection Law'
        analysis = 'Under the Consumer Protection Act 2019, consumers have the right to seek redressal for defective goods, deficient services, and unfair trade practices. The Act provides for a three-tier grievance redressal mechanism.'
        steps = [
            'Collect bills, receipts, and warranty documents',
            'Send a formal written complaint to the company',
            'File a case on the National Consumer Helpline',
            'Approach the District Consumer Disputes Redressal Forum',
        ]
    } else {
        area = 'General Legal Advisory'
        analysis = 'Thank you for sharing your situation. Based on your description, I\'ve identified potential legal aspects that may apply. For a more precise analysis, please share additional details such as dates, parties involved, and any documents you may have.'
        steps = [
            'Document all relevant facts and timeline',
            'Collect supporting evidence and correspondence',
            'Identify the relevant jurisdiction and authority',
            'Consult with a specialist lawyer in this area',
        ]
    }

    return { area, analysis, steps }
}

function ClientDashboard() {
    const navigate = useNavigate()
    const [messages, setMessages] = useState([])
    const [inputValue, setInputValue] = useState('')
    const [isTyping, setIsTyping] = useState(false)
    const [sidebarOpen, setSidebarOpen] = useState(true)
    const [activeSession, setActiveSession] = useState(null)
    const messagesEndRef = useRef(null)
    const textareaRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages, isTyping])

    const handleSend = (text) => {
        const query = text || inputValue.trim()
        if (!query || isTyping) return

        const userMessage = { type: 'user', text: query }
        setMessages((prev) => [...prev, userMessage])
        setInputValue('')
        setIsTyping(true)

        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'
        }

        // Simulate AI processing delay
        setTimeout(() => {
            const response = generateAIResponse(query)
            const aiMessage = { type: 'ai', ...response }
            setMessages((prev) => [...prev, aiMessage])
            setIsTyping(false)
        }, 1800)
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    const handleTextareaInput = (e) => {
        setInputValue(e.target.value)
        e.target.style.height = 'auto'
        e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
    }

    const handleNewCase = () => {
        setMessages([])
        setActiveSession(null)
        setInputValue('')
        setIsTyping(false)
    }

    const hasMessages = messages.length > 0

    return (
        <div className="dashboard-layout">
            {/* Sidebar */}
            <aside className={`dashboard-sidebar ${(!sidebarOpen || hasMessages) ? 'collapsed' : ''}`}>
                <div className="sidebar-header">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="w-7 h-7 rounded border border-[#c5a059] flex items-center justify-center">
                            <span className="text-[#c5a059] font-serif font-bold text-sm">A</span>
                        </div>
                        <Link to="/" className="text-lg font-bold tracking-widest text-white brand-font hover:text-[#c5a059] transition-colors">
                            ADAALAT
                        </Link>
                    </div>

                    <button className="new-case-btn" onClick={handleNewCase}>
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        New Case
                    </button>
                </div>

                <div className="sidebar-sessions">
                    {['Today', 'Yesterday', 'Last 7 days'].map((group) => {
                        const items = PAST_SESSIONS.filter((s) => s.date === group)
                        if (items.length === 0) return null
                        return (
                            <div key={group}>
                                <div className="session-group-label">{group}</div>
                                {items.map((session) => (
                                    <div
                                        key={session.id}
                                        className={`session-item ${activeSession === session.id ? 'active' : ''}`}
                                        onClick={() => setActiveSession(session.id)}
                                    >
                                        <svg className="w-4 h-4 flex-shrink-0 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                                        </svg>
                                        <span className="truncate">{session.title}</span>
                                    </div>
                                ))}
                            </div>
                        )
                    })}
                </div>

                <div className="sidebar-footer">
                    <div className="sidebar-user">
                        <div className="user-avatar">CL</div>
                        <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium text-white truncate">Client User</div>
                            <div className="text-xs text-gray-500 truncate">client@example.com</div>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Sidebar mobile overlay */}
            {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)}></div>}

            {/* Main Chat Area */}
            <div className="chat-main">
                {/* Header */}
                <div className="chat-header">
                    <div className="flex items-center gap-3">
                        <button
                            className="md:hidden text-gray-400 hover:text-white transition-colors"
                            onClick={() => setSidebarOpen(!sidebarOpen)}
                            aria-label="Toggle sidebar"
                        >
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
                            </svg>
                        </button>
                        <div>
                            <h2 className="text-sm font-semibold text-white">Legal Advisory</h2>
                            <p className="text-xs text-gray-500">AI-powered case analysis</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                        <span className="text-xs text-gray-500">Online</span>
                    </div>
                </div>

                {/* Messages or Welcome */}
                {!hasMessages ? (
                    <div className="welcome-container">
                        <div className="welcome-icon">
                            <svg className="w-8 h-8 text-[#c5a059]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                            </svg>
                        </div>
                        <h2 className="text-2xl md:text-3xl font-bold font-['Cinzel',serif] text-white mb-2">
                            How can I help you?
                        </h2>
                        <p className="text-gray-500 text-sm md:text-base max-w-md mb-8 leading-relaxed">
                            Describe your legal situation below. I'll analyze it and provide a preliminary advisory with relevant laws and next steps.
                        </p>

                        <div className="prompt-chips">
                            {SUGGESTED_PROMPTS.map((prompt) => (
                                <button
                                    key={prompt}
                                    className="prompt-chip"
                                    onClick={() => handleSend(prompt)}
                                >
                                    {prompt}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="chat-messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`chat-bubble ${msg.type}`}>
                                <div className={`bubble-label ${msg.type === 'user' ? 'user-label' : ''}`}>
                                    {msg.type === 'user' ? 'You' : 'Adaalat AI'}
                                </div>
                                {msg.type === 'user' ? (
                                    <div className="bubble-content">{msg.text}</div>
                                ) : (
                                    <div className="bubble-content">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-[#c5a059]/10 text-[#c5a059] border border-[#c5a059]/20">
                                                {msg.area}
                                            </span>
                                        </div>

                                        <p>{msg.analysis}</p>

                                        <div className="ai-section">
                                            <div className="ai-section-title">Recommended Next Steps</div>
                                            <ol className="list-decimal list-inside space-y-1 text-sm text-gray-400">
                                                {msg.steps.map((step, i) => (
                                                    <li key={i}>{step}</li>
                                                ))}
                                            </ol>
                                        </div>

                                        <div className="ai-disclaimer">
                                            <svg className="w-4 h-4 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                                            </svg>
                                            <span>
                                                This is an AI-generated preliminary advisory and does not constitute legal advice. Please consult a qualified lawyer for professional guidance.
                                            </span>
                                        </div>

                                        <button className="find-lawyer-btn" onClick={() => navigate('/find-lawyer', { state: { area: msg.area, query: messages.filter(m => m.type === 'user').slice(-1)[0]?.text || '' } })}>
                                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                            </svg>
                                            Find a Lawyer
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}

                        {isTyping && (
                            <div className="chat-bubble ai">
                                <div className="bubble-label">Adaalat AI</div>
                                <div className="typing-indicator">
                                    <div className="typing-dot"></div>
                                    <div className="typing-dot"></div>
                                    <div className="typing-dot"></div>
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>
                )}

                {/* Input Bar */}
                <div className="chat-input-bar">
                    <div className="chat-input-wrapper">
                        <textarea
                            ref={textareaRef}
                            className="chat-textarea"
                            placeholder="Describe your legal situation..."
                            value={inputValue}
                            onChange={handleTextareaInput}
                            onKeyDown={handleKeyDown}
                            rows={1}
                            disabled={isTyping}
                        />
                        <button
                            className="send-btn"
                            onClick={() => handleSend()}
                            disabled={!inputValue.trim() || isTyping}
                            aria-label="Send message"
                        >
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 12h14M12 5l7 7-7 7" />
                            </svg>
                        </button>
                    </div>
                    <div className="chat-input-hint">
                        Press Enter to send · Shift + Enter for new line
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ClientDashboard

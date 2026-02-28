import { useState } from 'react'
import { Link } from 'react-router-dom'
import './LawyerDashboard.css'

// ── Sample Data ───────────────────────────────────────────────
const sampleBriefs = [
    { id: 1, title: 'Tenant Eviction Dispute – Mumbai', client: 'Rajeev Mehta', priority: 'high', time: '2h ago' },
    { id: 2, title: 'Insurance Claim Rejection – HDFC', client: 'Sonal Kapoor', priority: 'medium', time: '4h ago' },
    { id: 3, title: 'Property Inheritance Query', client: 'Anil Sharma', priority: 'high', time: '5h ago' },
    { id: 4, title: 'Employment Contract Review', client: 'Priya Das', priority: 'low', time: '1d ago' },
]

const sampleSentItems = [
    { id: 1, name: 'Eviction_Response_Draft.pdf', client: 'Rajeev Mehta', date: 'Today, 2:30 PM', status: 'viewed' },
    { id: 2, name: 'Claim_Appeal_Letter.pdf', client: 'Sonal Kapoor', date: 'Yesterday', status: 'delivered' },
    { id: 3, name: 'Inheritance_Advisory.pdf', client: 'Anil Sharma', date: 'Feb 26', status: 'sent' },
]

const sampleDocuments = [
    { id: 1, name: 'Rental Agreement – Mehta vs. Builder Corp', type: 'Legal Notice', date: 'Feb 28, 2026', status: 'draft' },
    { id: 2, name: 'Insurance Appeal – HDFC Policy #4521', type: 'Appeal Letter', date: 'Feb 27, 2026', status: 'sent' },
    { id: 3, name: 'Property Transfer Deed – Sharma Estate', type: 'Transfer Deed', date: 'Feb 26, 2026', status: 'completed' },
    { id: 4, name: 'Employment NDA – TechStart Pvt Ltd', type: 'NDA', date: 'Feb 25, 2026', status: 'draft' },
    { id: 5, name: 'Court Filing – Consumer Forum Case', type: 'Court Filing', date: 'Feb 24, 2026', status: 'sent' },
]

// ── Icon Components ──────────────────────────────────────────
const Icons = {
    Dashboard: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" />
            <rect x="14" y="14" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" />
        </svg>
    ),
    Briefcase: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" /><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
        </svg>
    ),
    FileText: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><polyline points="10 9 9 9 8 9" />
        </svg>
    ),
    BarChart: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="20" x2="12" y2="10" /><line x1="18" y1="20" x2="18" y2="4" /><line x1="6" y1="20" x2="6" y2="16" />
        </svg>
    ),
    Settings: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
    ),
    Bell: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
    ),
    Search: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
    ),
    Send: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
        </svg>
    ),
    Plus: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
        </svg>
    ),
    Check: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
        </svg>
    ),
    X: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
        </svg>
    ),
    Menu: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="18" x2="21" y2="18" />
        </svg>
    ),
}

// ── LawyerDashboard Component ────────────────────────────────
function LawyerDashboard() {
    const [sidebarOpen, setSidebarOpen] = useState(false)
    const [activeNav, setActiveNav] = useState('Dashboard')

    const navMain = [
        { label: 'Dashboard', icon: Icons.Dashboard },
        { label: 'Smart Briefs', icon: Icons.Briefcase },
        { label: 'Documents', icon: Icons.FileText },
        { label: 'Analytics', icon: Icons.BarChart },
    ]

    const navSecondary = [
        { label: 'Settings', icon: Icons.Settings },
    ]

    return (
        <div className="lawyer-dashboard-layout">
            {/* ── Sidebar ── */}
            <aside className={`lawyer-sidebar ${sidebarOpen ? 'open' : ''}`}>
                <div className="lawyer-sidebar-brand">
                    <div className="lawyer-sidebar-brand-icon">A</div>
                    <Link to="/" className="lawyer-sidebar-brand-text">ADAALAT</Link>
                </div>

                <nav className="lawyer-sidebar-nav">
                    <span className="lawyer-sidebar-section-label">Main</span>
                    {navMain.map(item => (
                        <button
                            key={item.label}
                            className={`lawyer-sidebar-link ${activeNav === item.label ? 'active' : ''}`}
                            onClick={() => { setActiveNav(item.label); setSidebarOpen(false) }}
                        >
                            <item.icon />{item.label}
                        </button>
                    ))}

                    <span className="lawyer-sidebar-section-label">System</span>
                    {navSecondary.map(item => (
                        <button
                            key={item.label}
                            className={`lawyer-sidebar-link ${activeNav === item.label ? 'active' : ''}`}
                            onClick={() => { setActiveNav(item.label); setSidebarOpen(false) }}
                        >
                            <item.icon />{item.label}
                        </button>
                    ))}
                </nav>

                <div className="lawyer-sidebar-footer">
                    <div className="lawyer-sidebar-user">
                        <div className="lawyer-sidebar-avatar">AK</div>
                        <div className="lawyer-sidebar-user-info">
                            <div className="lawyer-sidebar-user-name">Adv. Arjun Khanna</div>
                            <div className="lawyer-sidebar-user-role">Senior Advocate</div>
                        </div>
                    </div>
                </div>
            </aside>

            {/* ── Mobile Toggle ── */}
            <button className="lawyer-sidebar-toggle" onClick={() => setSidebarOpen(!sidebarOpen)} aria-label="Toggle sidebar">
                <Icons.Menu />
            </button>

            {/* ── Main Content ── */}
            <main className="lawyer-main">
                {/* ── Top Bar ── */}
                <header className="lawyer-topbar">
                    <div className="lawyer-topbar-left">
                        <h1>Welcome back, Arjun 👋</h1>
                        <p>Here's what's happening with your practice today.</p>
                    </div>
                    <div className="lawyer-topbar-right">
                        <button className="lawyer-topbar-btn" aria-label="Search">
                            <Icons.Search />
                        </button>
                        <button className="lawyer-topbar-btn" aria-label="Notifications">
                            <Icons.Bell />
                            <span className="notification-dot"></span>
                        </button>
                        <div className="lawyer-topbar-avatar">AK</div>
                    </div>
                </header>

                <div className="lawyer-content">
                    {/* ── Stats Cards ── */}
                    <div className="lawyer-stats-grid">
                        {[
                            { value: '12', label: 'Active Cases', trend: '+3', dir: 'up', color: 'gold', icon: '⚖️' },
                            { value: '7', label: 'Pending Briefs', trend: '+2', dir: 'up', color: 'blue', icon: '📋' },
                            { value: '34', label: 'Documents Drafted', trend: '+8', dir: 'up', color: 'green', icon: '📄' },
                            { value: '21', label: 'Documents Sent', trend: '+5', dir: 'up', color: 'purple', icon: '📨' },
                        ].map((stat, i) => (
                            <div key={i} className="lawyer-stat-card lawyer-dashboard-animate">
                                <div className="lawyer-stat-card-header">
                                    <div className={`lawyer-stat-icon ${stat.color}`}>{stat.icon}</div>
                                    <span className={`lawyer-stat-trend ${stat.dir}`}>
                                        {stat.dir === 'up' ? '↑' : '↓'} {stat.trend}
                                    </span>
                                </div>
                                <div className="lawyer-stat-value">{stat.value}</div>
                                <div className="lawyer-stat-label">{stat.label}</div>
                            </div>
                        ))}
                    </div>

                    {/* ── Smart Briefs + Send Paperwork ── */}
                    <div className="lawyer-content-grid">
                        {/* Smart Briefs Feed */}
                        <div className="lawyer-glass-card lawyer-dashboard-animate">
                            <div className="lawyer-card-header">
                                <div className="lawyer-card-title">
                                    <Icons.Briefcase />
                                    Smart Briefs
                                </div>
                                <span className="lawyer-card-badge">{sampleBriefs.length} New</span>
                            </div>
                            <div className="lawyer-brief-list">
                                {sampleBriefs.map((brief, i) => (
                                    <div key={brief.id} className="lawyer-brief-item">
                                        <div className="lawyer-brief-number">{String(i + 1).padStart(2, '0')}</div>
                                        <div className="lawyer-brief-info">
                                            <div className="lawyer-brief-title">{brief.title}</div>
                                            <div className="lawyer-brief-meta">
                                                <span>{brief.client}</span>
                                                <span>•</span>
                                                <span>{brief.time}</span>
                                            </div>
                                        </div>
                                        <span className={`lawyer-brief-priority ${brief.priority}`}>{brief.priority}</span>
                                        <div className="lawyer-brief-actions">
                                            <button className="lawyer-btn-accept" title="Accept"><Icons.Check /></button>
                                            <button className="lawyer-btn-decline" title="Decline"><Icons.X /></button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Send Paperwork */}
                        <div className="lawyer-glass-card lawyer-dashboard-animate">
                            <div className="lawyer-card-header">
                                <div className="lawyer-card-title">
                                    <Icons.Send />
                                    Send Paperwork
                                </div>
                            </div>

                            <div className="lawyer-send-form">
                                <div className="lawyer-form-group">
                                    <label className="lawyer-form-label">Select Client</label>
                                    <select className="lawyer-form-select" defaultValue="">
                                        <option value="" disabled>Choose a client…</option>
                                        <option>Rajeev Mehta</option>
                                        <option>Sonal Kapoor</option>
                                        <option>Anil Sharma</option>
                                        <option>Priya Das</option>
                                    </select>
                                </div>

                                <div className="lawyer-form-group">
                                    <label className="lawyer-form-label">Attach Document</label>
                                    <div className="lawyer-file-upload-area">
                                        <div className="lawyer-file-upload-icon">📎</div>
                                        <div className="lawyer-file-upload-text">
                                            <span>Click to upload</span> or drag and drop
                                            <br />PDF, DOCX up to 10MB
                                        </div>
                                    </div>
                                </div>

                                <button className="lawyer-btn-send">
                                    <Icons.Send /> Send as PDF
                                </button>
                            </div>

                            <div className="lawyer-sent-items-header">Recent Sent Items</div>
                            {sampleSentItems.map(item => (
                                <div key={item.id} className="lawyer-sent-item">
                                    <div className="lawyer-sent-item-icon">📄</div>
                                    <div className="lawyer-sent-item-info">
                                        <div className="lawyer-sent-item-name">{item.name}</div>
                                        <div className="lawyer-sent-item-date">{item.client} · {item.date}</div>
                                    </div>
                                    <span className={`lawyer-delivery-status ${item.status}`}>{item.status}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* ── Recent Documents Table ── */}
                    <div className="lawyer-glass-card lawyer-dashboard-animate">
                        <div className="lawyer-card-header">
                            <div className="lawyer-card-title">
                                <Icons.FileText />
                                Recent Documents
                            </div>
                            <span className="lawyer-card-badge">{sampleDocuments.length} Total</span>
                        </div>
                        <div className="lawyer-documents-table-wrapper">
                            <table className="lawyer-documents-table">
                                <thead>
                                    <tr>
                                        <th>Document</th>
                                        <th>Type</th>
                                        <th>Date</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {sampleDocuments.map(doc => (
                                        <tr key={doc.id}>
                                            <td>
                                                <div className="lawyer-doc-name">
                                                    <div className="lawyer-doc-icon">📑</div>
                                                    {doc.name}
                                                </div>
                                            </td>
                                            <td>{doc.type}</td>
                                            <td>{doc.date}</td>
                                            <td>
                                                <span className={`lawyer-status-badge ${doc.status === 'sent' ? 'sent-status' : doc.status}`}>
                                                    {doc.status}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </main>

            {/* ── Quick Action FABs ── */}
            <div className="lawyer-quick-actions">
                <button className="lawyer-quick-action-btn primary" title="New Document">
                    <Icons.Plus />
                </button>
                <button className="lawyer-quick-action-btn" title="Send Paperwork">
                    <Icons.Send />
                </button>
            </div>
        </div>
    )
}

export default LawyerDashboard

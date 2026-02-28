import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import './FindLawyer.css'
import './LandingPage.css'

// ── Sample Lawyer Data (simulating RAG retrieval results) ──
const LAWYER_DATABASE = {
    'Tenancy & Property Law': [
        {
            id: 1, name: 'Adv. Meera Krishnan', initials: 'MK',
            specialization: 'Property & Real Estate Law',
            location: 'Mumbai, Maharashtra',
            barCouncil: 'Bar Council of Maharashtra & Goa',
            experience: 14, rating: 4.9, reviews: 127, matchScore: 97,
            casesWon: 312, online: true,
            tags: ['Tenant Rights', 'Rent Control Act', 'Property Disputes', 'Eviction Defense'],
        },
        {
            id: 2, name: 'Adv. Rajat Verma', initials: 'RV',
            specialization: 'Civil & Property Litigation',
            location: 'Delhi NCR',
            barCouncil: 'Bar Council of Delhi',
            experience: 11, rating: 4.7, reviews: 89, matchScore: 93,
            casesWon: 247, online: true,
            tags: ['Civil Litigation', 'Property Transfer', 'Landlord-Tenant', 'Injunctions'],
        },
        {
            id: 3, name: 'Adv. Sunita Iyer', initials: 'SI',
            specialization: 'Real Estate & Housing Law',
            location: 'Bangalore, Karnataka',
            barCouncil: 'Bar Council of Karnataka',
            experience: 9, rating: 4.6, reviews: 64, matchScore: 88,
            casesWon: 178, online: false,
            tags: ['RERA Compliance', 'Housing Disputes', 'Lease Agreements', 'Property Registration'],
        },
    ],
    'Employment & Labour Law': [
        {
            id: 4, name: 'Adv. Vikram Desai', initials: 'VD',
            specialization: 'Employment & Labour Law',
            location: 'Mumbai, Maharashtra',
            barCouncil: 'Bar Council of Maharashtra & Goa',
            experience: 16, rating: 4.8, reviews: 156, matchScore: 96,
            casesWon: 389, online: true,
            tags: ['Wrongful Termination', 'Labour Court', 'Employee Rights', 'POSH Act'],
        },
        {
            id: 5, name: 'Adv. Priti Nair', initials: 'PN',
            specialization: 'Corporate & Employment Law',
            location: 'Chennai, Tamil Nadu',
            barCouncil: 'Bar Council of Tamil Nadu',
            experience: 12, rating: 4.7, reviews: 98, matchScore: 91,
            casesWon: 267, online: true,
            tags: ['Contract Review', 'Salary Disputes', 'HR Compliance', 'Severance'],
        },
        {
            id: 6, name: 'Adv. Arjun Bhatt', initials: 'AB',
            specialization: 'Industrial & Labour Law',
            location: 'Ahmedabad, Gujarat',
            barCouncil: 'Bar Council of Gujarat',
            experience: 8, rating: 4.5, reviews: 52, matchScore: 85,
            casesWon: 134, online: false,
            tags: ['Industrial Disputes', 'Trade Unions', 'Gratuity', 'PF Claims'],
        },
    ],
    'Property & Real Estate Law': [
        {
            id: 7, name: 'Adv. Deepak Shetty', initials: 'DS',
            specialization: 'Property & Land Law',
            location: 'Pune, Maharashtra',
            barCouncil: 'Bar Council of Maharashtra & Goa',
            experience: 18, rating: 4.9, reviews: 201, matchScore: 98,
            casesWon: 456, online: true,
            tags: ['Title Disputes', 'Land Acquisition', 'Property Transfer', 'Boundary Disputes'],
        },
        {
            id: 8, name: 'Adv. Kavitha Reddy', initials: 'KR',
            specialization: 'Real Estate & Construction Law',
            location: 'Hyderabad, Telangana',
            barCouncil: 'Bar Council of Telangana',
            experience: 13, rating: 4.8, reviews: 112, matchScore: 94,
            casesWon: 298, online: true,
            tags: ['RERA', 'Construction Defects', 'Builder Disputes', 'Property Registration'],
        },
        {
            id: 9, name: 'Adv. Anand Kulkarni', initials: 'AK',
            specialization: 'Civil & Property Litigation',
            location: 'Bangalore, Karnataka',
            barCouncil: 'Bar Council of Karnataka',
            experience: 10, rating: 4.6, reviews: 76, matchScore: 87,
            casesWon: 198, online: false,
            tags: ['Partition Suits', 'Inheritance', 'Easement Rights', 'Encroachment'],
        },
    ],
    'Family Law': [
        {
            id: 10, name: 'Adv. Nandini Sharma', initials: 'NS',
            specialization: 'Family & Matrimonial Law',
            location: 'Delhi NCR',
            barCouncil: 'Bar Council of Delhi',
            experience: 15, rating: 4.9, reviews: 189, matchScore: 97,
            casesWon: 412, online: true,
            tags: ['Divorce', 'Custody', 'Alimony', 'Domestic Violence'],
        },
        {
            id: 11, name: 'Adv. Rohan Malhotra', initials: 'RM',
            specialization: 'Family Law & Mediation',
            location: 'Mumbai, Maharashtra',
            barCouncil: 'Bar Council of Maharashtra & Goa',
            experience: 12, rating: 4.7, reviews: 134, matchScore: 92,
            casesWon: 287, online: true,
            tags: ['Mediation', 'Child Custody', 'Maintenance', 'Hindu Marriage Act'],
        },
        {
            id: 12, name: 'Adv. Fatima Khan', initials: 'FK',
            specialization: 'Personal Law & Family Disputes',
            location: 'Lucknow, Uttar Pradesh',
            barCouncil: 'Bar Council of Uttar Pradesh',
            experience: 9, rating: 4.5, reviews: 67, matchScore: 86,
            casesWon: 156, online: false,
            tags: ['Muslim Personal Law', 'Succession', 'Guardianship', 'Nikah Disputes'],
        },
    ],
    'Cyber Crime & IT Law': [
        {
            id: 13, name: 'Adv. Siddharth Jain', initials: 'SJ',
            specialization: 'Cyber Law & Data Privacy',
            location: 'Bangalore, Karnataka',
            barCouncil: 'Bar Council of Karnataka',
            experience: 10, rating: 4.8, reviews: 91, matchScore: 96,
            casesWon: 203, online: true,
            tags: ['IT Act 2000', 'Online Fraud', 'Data Breach', 'Identity Theft'],
        },
        {
            id: 14, name: 'Adv. Pallavi Sen', initials: 'PS',
            specialization: 'Technology & Cyber Crime Law',
            location: 'Hyderabad, Telangana',
            barCouncil: 'Bar Council of Telangana',
            experience: 7, rating: 4.6, reviews: 48, matchScore: 90,
            casesWon: 112, online: true,
            tags: ['Cyber Stalking', 'Phishing', 'E-commerce Fraud', 'Social Media Crime'],
        },
        {
            id: 15, name: 'Adv. Manish Tiwari', initials: 'MT',
            specialization: 'Cyber Forensics & IT Litigation',
            location: 'Delhi NCR',
            barCouncil: 'Bar Council of Delhi',
            experience: 13, rating: 4.7, reviews: 79, matchScore: 87,
            casesWon: 167, online: false,
            tags: ['Digital Evidence', 'Hacking Cases', 'Cryptocurrency Fraud', 'IP Theft'],
        },
    ],
    'Consumer Protection Law': [
        {
            id: 16, name: 'Adv. Aisha Patel', initials: 'AP',
            specialization: 'Consumer Rights & Protection',
            location: 'Mumbai, Maharashtra',
            barCouncil: 'Bar Council of Maharashtra & Goa',
            experience: 11, rating: 4.8, reviews: 143, matchScore: 95,
            casesWon: 334, online: true,
            tags: ['Consumer Forum', 'Product Liability', 'Service Deficiency', 'Unfair Trade'],
        },
        {
            id: 17, name: 'Adv. Karthik Rajan', initials: 'KR',
            specialization: 'Consumer & Commercial Law',
            location: 'Chennai, Tamil Nadu',
            barCouncil: 'Bar Council of Tamil Nadu',
            experience: 9, rating: 4.6, reviews: 72, matchScore: 89,
            casesWon: 198, online: false,
            tags: ['NCDRC', 'Insurance Claims', 'Banking Disputes', 'E-commerce'],
        },
        {
            id: 18, name: 'Adv. Sneha Gupta', initials: 'SG',
            specialization: 'Consumer Dispute Resolution',
            location: 'Kolkata, West Bengal',
            barCouncil: 'Bar Council of West Bengal',
            experience: 8, rating: 4.5, reviews: 56, matchScore: 84,
            casesWon: 145, online: true,
            tags: ['Mediation', 'Class Action', 'Medical Negligence', 'Telecom Disputes'],
        },
    ],
    'General Legal Advisory': [
        {
            id: 19, name: 'Adv. Rahul Menon', initials: 'RM',
            specialization: 'General Practice & Civil Law',
            location: 'Kochi, Kerala',
            barCouncil: 'Bar Council of Kerala',
            experience: 20, rating: 4.9, reviews: 234, matchScore: 92,
            casesWon: 512, online: true,
            tags: ['Civil Suits', 'Contract Law', 'Legal Opinion', 'Arbitration'],
        },
        {
            id: 20, name: 'Adv. Tanvi Agarwal', initials: 'TA',
            specialization: 'Litigation & Advisory',
            location: 'Jaipur, Rajasthan',
            barCouncil: 'Bar Council of Rajasthan',
            experience: 14, rating: 4.7, reviews: 108, matchScore: 88,
            casesWon: 276, online: true,
            tags: ['Writ Petitions', 'RTI', 'Legal Drafting', 'Notary Services'],
        },
        {
            id: 21, name: 'Adv. Nikhil Saxena', initials: 'NS',
            specialization: 'Multi-Practice Law',
            location: 'Delhi NCR',
            barCouncil: 'Bar Council of Delhi',
            experience: 11, rating: 4.6, reviews: 87, matchScore: 83,
            casesWon: 224, online: false,
            tags: ['Criminal Law', 'Civil Law', 'Family Law', 'Corporate Matters'],
        },
    ],
}

const FILTER_OPTIONS = ['All', 'Highest Match', 'Most Experienced', 'Top Rated', 'Available Now']

// ── Star SVG component ──
function StarIcon({ filled }) {
    return (
        <svg
            className={`star ${filled ? 'filled' : ''}`}
            viewBox="0 0 24 24"
            fill={filled ? 'currentColor' : 'none'}
            stroke="currentColor"
            strokeWidth="1.5"
        >
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
        </svg>
    )
}

// ── Match Ring component ──
function MatchRing({ score }) {
    const radius = 24
    const circumference = 2 * Math.PI * radius
    const offset = circumference - (score / 100) * circumference

    return (
        <div className="match-ring">
            <svg width="56" height="56" viewBox="0 0 56 56">
                <circle className="match-ring-bg" cx="28" cy="28" r={radius} />
                <circle
                    className="match-ring-fill"
                    cx="28" cy="28" r={radius}
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                />
            </svg>
            <div className="match-ring-text">
                <span className="match-percentage">{score}%</span>
                <span className="match-label">Match</span>
            </div>
        </div>
    )
}

// ── Main Component ──
function FindLawyer() {
    const location = useLocation()
    const navigate = useNavigate()
    const { area, query } = location.state || {}

    const [loading, setLoading] = useState(true)
    const [lawyers, setLawyers] = useState([])
    const [activeFilter, setActiveFilter] = useState('All')
    const [connectedId, setConnectedId] = useState(null)
    const [toast, setToast] = useState(null)

    // Simulate RAG retrieval
    useEffect(() => {
        setLoading(true)
        const timer = setTimeout(() => {
            const matched = LAWYER_DATABASE[area] || LAWYER_DATABASE['General Legal Advisory']
            setLawyers(matched)
            setLoading(false)
        }, 2200)
        return () => clearTimeout(timer)
    }, [area])

    // Apply filter
    const getFilteredLawyers = () => {
        let result = [...lawyers]
        switch (activeFilter) {
            case 'Highest Match':
                result.sort((a, b) => b.matchScore - a.matchScore)
                break
            case 'Most Experienced':
                result.sort((a, b) => b.experience - a.experience)
                break
            case 'Top Rated':
                result.sort((a, b) => b.rating - a.rating)
                break
            case 'Available Now':
                result = result.filter(l => l.online)
                break
            default:
                break
        }
        return result
    }

    const handleConnect = (lawyer) => {
        setConnectedId(lawyer.id)
        setToast({
            name: lawyer.name,
            message: 'Connection request sent! The lawyer will respond within 24 hours.',
        })
        setTimeout(() => setToast(null), 4000)
    }

    const filteredLawyers = getFilteredLawyers()

    // ── No context passed — show empty state ──
    if (!area && !query) {
        return (
            <div className="find-lawyer-page">
                <div className="find-lawyer-main">
                    <header className="find-lawyer-header">
                        <div className="fl-header-left">
                            <button className="fl-back-btn" onClick={() => navigate('/dashboard')}>
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M19 12H5" /><polyline points="12 19 5 12 12 5" />
                                </svg>
                            </button>
                            <div className="fl-header-title">
                                <h1>Find a Lawyer</h1>
                                <p>AI-powered lawyer matching</p>
                            </div>
                        </div>
                    </header>
                    <div className="empty-state">
                        <div className="empty-state-icon">⚖️</div>
                        <h3>No Case Context Found</h3>
                        <p>Start by describing your legal situation in the Client Dashboard. Our AI will analyze your case and find the best matching lawyers for you.</p>
                        <button className="btn-go-back" onClick={() => navigate('/dashboard')}>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="16" height="16">
                                <path d="M19 12H5" /><polyline points="12 19 5 12 12 5" />
                            </svg>
                            Go to Dashboard
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="find-lawyer-page">
            <div className="find-lawyer-main">
                {/* ── Header ── */}
                <header className="find-lawyer-header">
                    <div className="fl-header-left">
                        <button className="fl-back-btn" onClick={() => navigate(-1)}>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M19 12H5" /><polyline points="12 19 5 12 12 5" />
                            </svg>
                        </button>
                        <div className="fl-header-title">
                            <h1>Find Your Lawyer</h1>
                            <p>Top matches powered by AI retrieval</p>
                        </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#34d399', animation: 'spin 2s linear infinite' }}></div>
                        <span style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.4)' }}>RAG Engine Active</span>
                    </div>
                </header>

                <div className="find-lawyer-content">
                    {/* ── Case Context Card ── */}
                    <div className="case-context-card">
                        <div className="case-context-icon">⚖️</div>
                        <div className="case-context-info">
                            <div className="case-context-area">{area}</div>
                            <div className="case-context-query">{query}</div>
                        </div>
                    </div>

                    {loading ? (
                        /* ── Loading State ── */
                        <div>
                            <div className="loading-container">
                                <div className="loading-spinner"></div>
                                <div className="loading-text">Searching for the best lawyers…</div>
                                <div className="loading-subtext">Analyzing specialization, experience, and case relevance</div>
                            </div>
                            <div className="skeleton-grid">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="skeleton-card">
                                        <div className="skeleton-top">
                                            <div className="skeleton-avatar"></div>
                                            <div className="skeleton-lines">
                                                <div className="skeleton-line" style={{ width: '70%' }}></div>
                                                <div className="skeleton-line" style={{ width: '50%' }}></div>
                                                <div className="skeleton-line" style={{ width: '40%' }}></div>
                                            </div>
                                        </div>
                                        <div className="skeleton-line" style={{ width: '100%' }}></div>
                                        <div className="skeleton-line" style={{ width: '80%' }}></div>
                                        <div className="skeleton-line" style={{ width: '60%', height: '36px', borderRadius: '8px' }}></div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ) : (
                        /* ── Results ── */
                        <>
                            {/* Filter Bar */}
                            <div className="filter-bar">
                                <span className="filter-label">Sort by</span>
                                {FILTER_OPTIONS.map(opt => (
                                    <button
                                        key={opt}
                                        className={`filter-chip ${activeFilter === opt ? 'active' : ''}`}
                                        onClick={() => setActiveFilter(opt)}
                                    >
                                        {opt}
                                    </button>
                                ))}
                            </div>

                            {/* Results Header */}
                            <div className="results-header">
                                <div className="results-title">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c5a059" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                                        <circle cx="9" cy="7" r="4" />
                                        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                                        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                                    </svg>
                                    Top Lawyer Recommendations
                                </div>
                                <span className="results-count">{filteredLawyers.length} Found</span>
                            </div>

                            {/* Lawyer Cards Grid */}
                            <div className="lawyer-grid">
                                {filteredLawyers.map(lawyer => (
                                    <div key={lawyer.id} className="lawyer-card">
                                        <div className="lawyer-card-top">
                                            <div className="lawyer-avatar">
                                                {lawyer.initials}
                                                {lawyer.online && <div className="online-dot"></div>}
                                            </div>
                                            <div className="lawyer-info">
                                                <div className="lawyer-name">{lawyer.name}</div>
                                                <div className="lawyer-specialization">{lawyer.specialization}</div>
                                                <div className="lawyer-location">
                                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                                                        <circle cx="12" cy="10" r="3" />
                                                    </svg>
                                                    {lawyer.location}
                                                </div>
                                            </div>
                                            <MatchRing score={lawyer.matchScore} />
                                        </div>

                                        {/* Stats Row */}
                                        <div className="lawyer-stats">
                                            <div className="lawyer-stat">
                                                <span className="lawyer-stat-icon">📅</span>
                                                <span className="lawyer-stat-value">{lawyer.experience}</span>
                                                <span className="lawyer-stat-label">yrs exp</span>
                                            </div>
                                            <div className="lawyer-stat">
                                                <span className="lawyer-stat-icon">🏆</span>
                                                <span className="lawyer-stat-value">{lawyer.casesWon}</span>
                                                <span className="lawyer-stat-label">cases</span>
                                            </div>
                                            <div className="lawyer-stat">
                                                <div className="star-rating">
                                                    {[1, 2, 3, 4, 5].map(s => (
                                                        <StarIcon key={s} filled={s <= Math.round(lawyer.rating)} />
                                                    ))}
                                                </div>
                                                <span className="rating-text">{lawyer.rating}</span>
                                                <span className="review-count">({lawyer.reviews})</span>
                                            </div>
                                        </div>

                                        {/* Practice Area Tags */}
                                        <div className="practice-tags">
                                            {lawyer.tags.map((tag, i) => (
                                                <span key={tag} className={`practice-tag ${i === 0 ? 'primary' : ''}`}>{tag}</span>
                                            ))}
                                        </div>

                                        {/* Actions */}
                                        <div className="lawyer-card-actions">
                                            <button
                                                className="btn-connect"
                                                onClick={() => handleConnect(lawyer)}
                                                disabled={connectedId === lawyer.id}
                                                style={connectedId === lawyer.id ? { opacity: 0.6, cursor: 'default', background: 'rgba(16,185,129,0.2)', color: '#34d399' } : {}}
                                            >
                                                {connectedId === lawyer.id ? (
                                                    <>
                                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                                            <polyline points="20 6 9 17 4 12" />
                                                        </svg>
                                                        Connected
                                                    </>
                                                ) : (
                                                    <>
                                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" />
                                                        </svg>
                                                        Connect
                                                    </>
                                                )}
                                            </button>
                                            <button className="btn-view-profile">
                                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                                    <circle cx="12" cy="12" r="3" />
                                                </svg>
                                                View Profile
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Powered By */}
                            <div className="powered-by">
                                Recommendations powered by <span>Adaalat RAG Engine</span> · Matching based on specialization, experience, and case relevance
                            </div>
                        </>
                    )}
                </div>
            </div>

            {/* ── Toast Notification ── */}
            {toast && (
                <div className="toast-notification">
                    <div className="toast-icon">✅</div>
                    <div className="toast-content">
                        <div className="toast-title">{toast.name}</div>
                        <div className="toast-message">{toast.message}</div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default FindLawyer

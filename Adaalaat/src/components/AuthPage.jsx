import { useState } from 'react'
import { Link, useSearchParams, useNavigate } from 'react-router-dom'
import './AuthPage.css'
import './LandingPage.css'

function AuthPage() {
    const [searchParams] = useSearchParams()
    const initialMode = searchParams.get('mode') === 'signup' ? 'signup' : 'login'
    const [mode, setMode] = useState(initialMode)
    const navigate = useNavigate()

    // Login form state
    const [loginData, setLoginData] = useState({ email: '', password: '' })

    // Signup form state
    const [signupData, setSignupData] = useState({
        fullName: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        role: '',
        barRegistration: '',
        portfolioUrl: '',
    })

    const handleLoginChange = (e) => {
        setLoginData({ ...loginData, [e.target.name]: e.target.value })
    }

    const handleSignupChange = (e) => {
        setSignupData({ ...signupData, [e.target.name]: e.target.value })
    }

    const handleLoginSubmit = (e) => {
        e.preventDefault()
        console.log('Login submitted:', loginData)
        navigate('/dashboard')
    }

    const handleSignupSubmit = (e) => {
        e.preventDefault()
        console.log('Signup submitted:', signupData)
        if (signupData.role === 'client') {
            navigate('/dashboard')
        } else {
            navigate('/dashboard')
        }
    }

    return (
        <div className="relative min-h-screen flex flex-col font-['Inter',sans-serif] bg-[var(--color-dark)] text-[var(--color-cream)] selection:bg-yellow-900 selection:text-white">

            {/* Noise Texture Overlay */}
            <div className="bg-noise"></div>

            {/* Background decorative gradients */}
            <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[35%] h-[35%] bg-yellow-900/10 rounded-full blur-[120px]"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[35%] h-[35%] bg-amber-900/10 rounded-full blur-[120px]"></div>
                <div className="absolute top-[30%] right-[10%] w-[20%] h-[20%] bg-[#c5a059]/5 rounded-full blur-[100px]"></div>
            </div>

            {/* Navigation */}
            <nav className="relative z-50 w-full px-6 py-6 md:px-12 flex justify-between items-center border-b border-white/5 bg-[#0f0c08]/80 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded border border-[#c5a059] flex items-center justify-center">
                        <span className="text-[#c5a059] font-serif font-bold text-lg">A</span>
                    </div>
                    <Link to="/" className="text-2xl md:text-3xl font-bold tracking-widest text-white brand-font hover:text-[#c5a059] transition-colors duration-300">
                        ADAALAT
                    </Link>
                </div>

                <Link to="/" className="text-sm font-medium text-gray-400 hover:text-[#c5a059] transition-colors flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Back to Home
                </Link>
            </nav>

            {/* Main Content */}
            <main className="relative z-10 flex-grow flex items-center justify-center px-6 py-12 md:py-16">
                <div className="w-full max-w-md">

                    {/* Auth Card */}
                    <div className="auth-card auth-card-glow rounded-lg border border-white/5 bg-[#0f0c08]/60 backdrop-blur-xl p-8 md:p-10">

                        {/* Logo/Header */}
                        <div className="text-center mb-8">
                            <div className="w-14 h-14 rounded-lg border border-[#c5a059]/30 flex items-center justify-center mx-auto mb-4 bg-[#c5a059]/5">
                                <span className="text-[#c5a059] font-serif font-bold text-2xl">A</span>
                            </div>
                            <h1 className="text-xl font-bold font-['Cinzel',serif] tracking-wider text-white">
                                {mode === 'login' ? 'Welcome Back' : 'Create Account'}
                            </h1>
                            <p className="text-gray-500 text-sm mt-2">
                                {mode === 'login'
                                    ? 'Enter your credentials to access your account'
                                    : 'Join the digital justice platform'}
                            </p>
                        </div>

                        {/* Toggle Tabs */}
                        <div className="flex justify-center mb-8 border-b border-white/5">
                            <button
                                className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
                                onClick={() => setMode('login')}
                            >
                                Login
                            </button>
                            <button
                                className={`auth-tab ${mode === 'signup' ? 'active' : ''}`}
                                onClick={() => setMode('signup')}
                            >
                                Sign Up
                            </button>
                        </div>

                        {/* Login Form */}
                        {mode === 'login' && (
                            <form onSubmit={handleLoginSubmit} className="space-y-5 form-slide-enter">
                                <div>
                                    <label className="auth-label" htmlFor="login-email">Email Address</label>
                                    <input
                                        id="login-email"
                                        type="email"
                                        name="email"
                                        className="auth-input"
                                        placeholder="you@example.com"
                                        value={loginData.email}
                                        onChange={handleLoginChange}
                                        required
                                    />
                                </div>

                                <div>
                                    <div className="flex justify-between items-center mb-1">
                                        <label className="auth-label" htmlFor="login-password" style={{ marginBottom: 0 }}>Password</label>
                                        <a href="#" className="text-xs text-[#c5a059]/70 hover:text-[#c5a059] transition-colors">
                                            Forgot password?
                                        </a>
                                    </div>
                                    <input
                                        id="login-password"
                                        type="password"
                                        name="password"
                                        className="auth-input"
                                        placeholder="••••••••"
                                        value={loginData.password}
                                        onChange={handleLoginChange}
                                        required
                                    />
                                </div>

                                <button type="submit" className="auth-submit-btn mt-2">
                                    Sign In
                                </button>

                                <div className="auth-divider">
                                    <span>or continue with</span>
                                </div>

                                <button type="button" className="social-btn">
                                    <svg className="w-5 h-5" viewBox="0 0 24 24">
                                        <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
                                        <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                                        <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                                        <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                                    </svg>
                                    Google
                                </button>

                                <p className="text-center text-gray-500 text-sm">
                                    Don't have an account?{' '}
                                    <button type="button" onClick={() => setMode('signup')} className="text-[#c5a059] hover:underline font-medium bg-transparent border-none cursor-pointer">
                                        Sign up
                                    </button>
                                </p>
                            </form>
                        )}

                        {/* Signup Form */}
                        {mode === 'signup' && (
                            <form onSubmit={handleSignupSubmit} className="space-y-4 form-slide-enter">
                                <div>
                                    <label className="auth-label" htmlFor="signup-name">Full Name</label>
                                    <input
                                        id="signup-name"
                                        type="text"
                                        name="fullName"
                                        className="auth-input"
                                        placeholder="John Doe"
                                        value={signupData.fullName}
                                        onChange={handleSignupChange}
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="auth-label" htmlFor="signup-email">Email Address</label>
                                    <input
                                        id="signup-email"
                                        type="email"
                                        name="email"
                                        className="auth-input"
                                        placeholder="you@example.com"
                                        value={signupData.email}
                                        onChange={handleSignupChange}
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="auth-label" htmlFor="signup-phone">Phone Number</label>
                                    <input
                                        id="signup-phone"
                                        type="tel"
                                        name="phone"
                                        className="auth-input"
                                        placeholder="+91 98765 43210"
                                        value={signupData.phone}
                                        onChange={handleSignupChange}
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="auth-label" htmlFor="signup-role">I am a</label>
                                    <div className="relative">
                                        <select
                                            id="signup-role"
                                            name="role"
                                            className="auth-select"
                                            value={signupData.role}
                                            onChange={handleSignupChange}
                                            required
                                        >
                                            <option value="" disabled>Select your role...</option>
                                            <option value="client">Client — Looking for legal help</option>
                                            <option value="lawyer">Lawyer — Offering legal services</option>
                                        </select>
                                        <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                        </svg>
                                    </div>
                                </div>

                                {signupData.role === 'lawyer' && (
                                    <>
                                        <div>
                                            <label className="auth-label" htmlFor="signup-bar">Bar Registration Number</label>
                                            <input
                                                id="signup-bar"
                                                type="text"
                                                name="barRegistration"
                                                className="auth-input"
                                                placeholder="e.g. BCI/MAH/12345/2020"
                                                value={signupData.barRegistration}
                                                onChange={handleSignupChange}
                                                required
                                            />
                                        </div>

                                        <div>
                                            <label className="auth-label" htmlFor="signup-portfolio">Portfolio Website</label>
                                            <input
                                                id="signup-portfolio"
                                                type="url"
                                                name="portfolioUrl"
                                                className="auth-input"
                                                placeholder="https://yourportfolio.com"
                                                value={signupData.portfolioUrl}
                                                onChange={handleSignupChange}
                                                required
                                            />
                                        </div>
                                    </>
                                )}

                                <div>
                                    <label className="auth-label" htmlFor="signup-password">Password</label>
                                    <input
                                        id="signup-password"
                                        type="password"
                                        name="password"
                                        className="auth-input"
                                        placeholder="••••••••"
                                        value={signupData.password}
                                        onChange={handleSignupChange}
                                        required
                                        minLength={8}
                                    />
                                </div>

                                <div>
                                    <label className="auth-label" htmlFor="signup-confirm">Confirm Password</label>
                                    <input
                                        id="signup-confirm"
                                        type="password"
                                        name="confirmPassword"
                                        className="auth-input"
                                        placeholder="••••••••"
                                        value={signupData.confirmPassword}
                                        onChange={handleSignupChange}
                                        required
                                        minLength={8}
                                    />
                                </div>

                                <div className="flex items-start gap-2 pt-1">
                                    <input type="checkbox" id="terms" required className="mt-1 accent-[#c5a059]" />
                                    <label htmlFor="terms" className="text-xs text-gray-500 leading-relaxed">
                                        I agree to the{' '}
                                        <a href="#" className="text-[#c5a059]/70 hover:text-[#c5a059] underline">Terms of Service</a>{' '}
                                        and{' '}
                                        <a href="#" className="text-[#c5a059]/70 hover:text-[#c5a059] underline">Privacy Policy</a>
                                    </label>
                                </div>

                                <button type="submit" className="auth-submit-btn mt-2">
                                    Create Account
                                </button>

                                <div className="auth-divider">
                                    <span>or continue with</span>
                                </div>

                                <button type="button" className="social-btn">
                                    <svg className="w-5 h-5" viewBox="0 0 24 24">
                                        <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
                                        <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                                        <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                                        <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                                    </svg>
                                    Google
                                </button>

                                <p className="text-center text-gray-500 text-sm">
                                    Already have an account?{' '}
                                    <button type="button" onClick={() => setMode('login')} className="text-[#c5a059] hover:underline font-medium bg-transparent border-none cursor-pointer">
                                        Sign in
                                    </button>
                                </p>
                            </form>
                        )}
                    </div>

                    {/* Footer text */}
                    <p className="text-center text-gray-600 text-xs mt-6">
                        &copy; {new Date().getFullYear()} Adaalat Legal Technologies. All Rights Reserved.
                    </p>
                </div>
            </main>
        </div>
    )
}

export default AuthPage

import './LandingPage.css'

function LandingPage() {
    return (
        <div className="relative min-h-screen flex flex-col selection:bg-yellow-900 selection:text-white font-['Inter',sans-serif] bg-[var(--color-dark)] text-[var(--color-cream)]">

            {/* Noise Texture Overlay */}
            <div className="bg-noise"></div>

            {/* Background decorative gradients */}
            <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-yellow-900/10 rounded-full blur-[120px]"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-amber-900/10 rounded-full blur-[120px]"></div>
            </div>

            {/* Navigation */}
            <nav className="relative z-50 w-full px-6 py-6 md:px-12 flex justify-between items-center border-b border-white/5 bg-[#0f0c08]/80 backdrop-blur-md sticky top-0">
                <div className="flex items-center gap-3">
                    {/* Mini Logo Icon */}
                    <div className="w-8 h-8 rounded border border-[#c5a059] flex items-center justify-center">
                        <span className="text-[#c5a059] font-serif font-bold text-lg">A</span>
                    </div>
                    <a href="#" className="text-2xl md:text-3xl font-bold tracking-widest text-white brand-font hover:text-[#c5a059] transition-colors duration-300">
                        ADAALAT
                    </a>
                </div>

                <div className="hidden md:flex items-center gap-6">
                    <a href="#" className="text-sm font-medium text-gray-400 hover:text-[#c5a059] transition-colors">How it Works</a>
                    <a href="#" className="text-sm font-medium text-gray-400 hover:text-[#c5a059] transition-colors">Services</a>

                    <div className="h-4 w-px bg-white/10"></div>

                    <a href="#" className="text-sm font-semibold text-white hover:text-[#c5a059] transition-colors px-2">Login</a>
                    <a href="#" className="glass-btn px-6 py-2 rounded-sm text-[#c5a059] text-sm font-semibold tracking-wide uppercase">
                        Sign Up
                    </a>
                </div>

                {/* Mobile Menu Button */}
                <button className="md:hidden text-white hover:text-[#c5a059]" aria-label="Open menu">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
                    </svg>
                </button>
            </nav>

            {/* Main Content */}
            <main className="relative z-10 flex-grow flex flex-col lg:flex-row items-center justify-center px-6 md:px-12 py-12 lg:py-0 max-w-7xl mx-auto w-full gap-12 lg:gap-0">

                {/* Left Text Section */}
                <div className="w-full lg:w-1/2 flex flex-col items-center lg:items-start text-center lg:text-left order-2 lg:order-1 space-y-8">
                    <div className="space-y-4">
                        <div className="inline-block px-3 py-1 border border-[#c5a059]/30 rounded-full bg-[#c5a059]/5 mb-2 fade-in-up">
                            <span className="text-[#c5a059] text-xs font-semibold tracking-widest uppercase">The Future of Law</span>
                        </div>

                        <h1 className="text-4xl md:text-6xl lg:text-7xl leading-tight font-bold font-['Cinzel',serif] fade-in-up delay-100">
                            Justice <br />
                            <span className="gold-gradient-text">Delivered.</span>
                        </h1>

                        <p className="text-gray-400 text-lg md:text-xl max-w-lg mx-auto lg:mx-0 font-light leading-relaxed fade-in-up delay-200">
                            A secure, transparent, and efficient platform connecting you to the legal system. Log in to manage your cases or sign up to find representation.
                        </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto fade-in-up delay-300">
                        <button className="bg-[#c5a059] hover:bg-[#b08d4b] text-[#0f0c08] px-8 py-4 rounded-sm font-bold tracking-wide transition-all transform hover:scale-105 shadow-[0_0_20px_rgba(197,160,89,0.3)]">
                            Get Started
                        </button>
                        <button className="border border-white/20 hover:border-[#c5a059] text-white hover:text-[#c5a059] px-8 py-4 rounded-sm font-semibold tracking-wide transition-all hover:bg-white/5">
                            Consult an Expert
                        </button>
                    </div>

                    <div className="flex items-center gap-6 pt-4 fade-in-up delay-300">
                        <div className="flex -space-x-3">
                            <div className="w-10 h-10 rounded-full bg-gray-700 border-2 border-[#0f0c08]"></div>
                            <div className="w-10 h-10 rounded-full bg-gray-600 border-2 border-[#0f0c08]"></div>
                            <div className="w-10 h-10 rounded-full bg-gray-500 border-2 border-[#0f0c08]"></div>
                        </div>
                        <div className="text-sm text-gray-400">
                            <span className="text-white font-bold">2,000+</span> Lawyers Active
                        </div>
                    </div>
                </div>

                {/* Right Graphic Section (Scales) */}
                <div className="w-full lg:w-1/2 flex justify-center items-center order-1 lg:order-2">
                    <div className="scales-container relative w-full max-w-[500px] aspect-square">
                        {/* Glowing backdrop behind scales */}
                        <div className="absolute inset-0 bg-gradient-to-tr from-[#c5a059]/20 to-transparent rounded-full blur-3xl transform scale-75"></div>

                        {/* Scales SVG */}
                        <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" className="w-full h-full svg-glow">
                            {/* Definitions for gradients */}
                            <defs>
                                <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" style={{ stopColor: '#f8e7b9', stopOpacity: 1 }} />
                                    <stop offset="50%" style={{ stopColor: '#c5a059', stopOpacity: 1 }} />
                                    <stop offset="100%" style={{ stopColor: '#8a6e36', stopOpacity: 1 }} />
                                </linearGradient>
                                <filter id="shadow">
                                    <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#000" floodOpacity="0.5" />
                                </filter>
                            </defs>

                            {/* Central Pole Group */}
                            <g transform="translate(200, 380)">
                                {/* Base */}
                                <path d="M-40,0 Q0,-20 40,0 L50,10 L-50,10 Z" fill="url(#goldGrad)" />
                                {/* Pillar */}
                                <rect x="-4" y="-340" width="8" height="350" fill="url(#goldGrad)" />
                                {/* Top Finial */}
                                <circle cx="0" cy="-350" r="10" fill="url(#goldGrad)" />
                            </g>

                            {/* Animation Container: pivot at top of pole */}
                            <g transform="translate(200, 40)">
                                {/* Rotatable Beam Group */}
                                <g className="balance-beam">
                                    {/* The Horizontal Beam */}
                                    <path d="M-140,0 L140,0 L135,5 L-135,5 Z" fill="url(#goldGrad)" filter="url(#shadow)" />
                                    <circle cx="0" cy="2" r="6" fill="#fff" stroke="#c5a059" strokeWidth="2" />

                                    {/* Left Pan Assembly */}
                                    <g transform="translate(-130, 0)">
                                        <g className="pan-item">
                                            <line x1="0" y1="0" x2="-30" y2="100" stroke="#e6c888" strokeWidth="1.5" />
                                            <line x1="0" y1="0" x2="30" y2="100" stroke="#e6c888" strokeWidth="1.5" />
                                            <line x1="0" y1="0" x2="0" y2="100" stroke="#e6c888" strokeWidth="1.5" />
                                            <path d="M-35,100 Q0,135 35,100 Z" fill="url(#goldGrad)" opacity="0.9" />
                                        </g>
                                    </g>

                                    {/* Right Pan Assembly */}
                                    <g transform="translate(130, 0)">
                                        <g className="pan-item">
                                            <line x1="0" y1="0" x2="-30" y2="100" stroke="#e6c888" strokeWidth="1.5" />
                                            <line x1="0" y1="0" x2="30" y2="100" stroke="#e6c888" strokeWidth="1.5" />
                                            <line x1="0" y1="0" x2="0" y2="100" stroke="#e6c888" strokeWidth="1.5" />
                                            <path d="M-35,100 Q0,135 35,100 Z" fill="url(#goldGrad)" opacity="0.9" />
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </svg>
                    </div>
                </div>

            </main>

            {/* Footer */}
            <footer className="relative z-10 w-full py-6 text-center border-t border-white/5 text-gray-500 text-xs md:text-sm">
                <p>&copy; {new Date().getFullYear()} Adaalat Legal Technologies. All Rights Reserved.</p>
            </footer>

        </div>
    )
}

export default LandingPage

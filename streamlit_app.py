import streamlit as st
import time
from datetime import datetime, timedelta
import requests
from urllib.parse import quote_plus
import asyncio
from agents.agents import agent_handler

# Page configuration
st.set_page_config(
    page_title="SpamX - Anti-Spam Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default elements completely
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
.stDecoration {display:none;}
.css-1d391kg {display:none;}
.css-12oz5g7 {display:none;}
.css-1rs6os {display:none;}
.css-2trqyj {display:none;}
.css-1v0mbdj {display:none;}
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}

.main > .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    margin-top: 0rem !important;
    margin-bottom: 0rem !important;
}
.stApp {
    background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3a 50%, #2a1a4a 100%);
    color: white;
}
.main .block-container {
    background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3a 50%, #2a1a4a 100%);
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Enhanced Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3a 30%, #2a1a4a 70%, #3a1a5a 100%);
        margin: 0;
        padding: 0;
        min-height: 100vh;
        overflow-x: hidden;
    }
    
    /* Animated background particles */
    .mobile-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 90% 70%, rgba(199, 125, 255, 0.04) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-20px) rotate(120deg); }
        66% { transform: translateY(10px) rotate(240deg); }
    }
    
    .mobile-container {
        background: transparent;
        min-height: 100vh;
        padding: 0;
        margin: 0;
        width: 100%;
        overflow-x: hidden;
        position: relative;
    }
    
    /* Enhanced header with glassmorphism and glow effects */
    .app-header {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.9) 0%, 
            rgba(139, 92, 246, 0.85) 30%, 
            rgba(236, 72, 153, 0.8) 70%, 
            rgba(251, 146, 60, 0.75) 100%);
        padding: 60px 30px;
        color: white;
        text-align: center;
        margin: 0;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 
            0 25px 80px rgba(99, 102, 241, 0.4), 
            0 12px 48px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(255,255,255,0.2);
        backdrop-filter: blur(30px);
        border-bottom: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
    }
    
    /* Animated geometric patterns */
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M50 50c0-5.5-4.5-10-10-10s-10 4.5-10 10 4.5 10 10 10 10-4.5 10-10zM10 10c0-5.5-4.5-10-10-10s-10 4.5-10 10 4.5 10 10 10 10-4.5 10-10zm40 40c0-5.5-4.5-10-10-10s-10 4.5-10 10 4.5 10 10 10 10-4.5 10-10z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.1;
        animation: slide 25s linear infinite;
        pointer-events: none;
    }
    
    /* Floating orbs */
    .app-header::after {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
        top: -150px;
        right: -150px;
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes slide {
        0% { transform: translateX(-25px) translateY(-25px) rotate(0deg); }
        100% { transform: translateX(25px) translateY(25px) rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: scale(0.8) rotate(0deg);
            opacity: 0.3;
        }
        50% { 
            transform: scale(1.2) rotate(180deg);
            opacity: 0.6;
        }
    }
    
    .app-header h1 {
        margin: 0;
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.8),
            0 4px 12px rgba(0,0,0,0.4),
            0 8px 24px rgba(99,102,241,0.6);
        background: linear-gradient(45deg, 
            #ffffff 0%, 
            #f0f0f0 25%, 
            #ffffff 50%, 
            #e0e0e0 75%, 
            #ffffff 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shimmer 3s linear infinite;
        position: relative;
        z-index: 1;
        letter-spacing: 2px;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .app-header p {
        margin: 25px 0 0 0;
        opacity: 0.95;
        font-style: italic;
        font-size: 1.5rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
        letter-spacing: 1px;
    }

    /* Enhanced disclaimer */
    .disclaimer-section {
        background: linear-gradient(135deg, 
            rgba(220, 38, 38, 0.95) 0%, 
            rgba(239, 68, 68, 0.9) 30%, 
            rgba(234, 88, 12, 0.85) 70%, 
            rgba(251, 146, 60, 0.8) 100%);
        padding: 30px;
        margin: 0;
        color: white;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        box-shadow: 
            0 8px 24px rgba(220, 38, 38, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        backdrop-filter: blur(20px);
    }
    
    .disclaimer-section h Peregrine3 {
        margin: 0 0 15px 0;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .disclaimer-section p {
        margin: 8px 0;
        font-size: 1rem;
        opacity: 0.95;
        line-height: 1.4;
    }
    
    .content-wrapper {
        padding: 40px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Enhanced search section with holographic effect */
    .google-search-section {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.9) 0%, 
            rgba(15, 23, 42, 0.8) 50%, 
            rgba(30, 41, 59, 0.7) 100%);
        border-radius: 28px;
        padding: 45px;
        margin: 40px 0;
        box-shadow: 
            0 25px 80px rgba(0,0,0,0.5), 
            0 12px 40px rgba(99,102,241,0.2),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(30px);
    }
    
    .google-search-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(99,102,241,0.8), 
            rgba(139,92,246,0.8), 
            transparent);
        animation: scan 3s ease-in-out infinite;
    }
    
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .search-container {
        position: relative;
        margin: 25px 0;
    }
    
    .search-box {
        width: 100%;
        padding: 25px 70px 25px 30px;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,255,255,0.05) 100%);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        color: white;
        font-size: 18px;
        font-weight: 500;
        backdrop-filter: blur(30px);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            inset 0 2px 10px rgba(0,0,0,0.1),
            0 4px 20px rgba(0,0,0,0.1);
    }
    
    .search-box::placeholder {
        color: rgba(255,255,255,0.7);
        font-style: italic;
    }
    
    .search-box:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 
            0 0 0 6px rgba(99, 102, 241, 0.15), 
            0 12px 40px rgba(99, 102, 241, 0.3),
            inset 0 2px 10px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.15) 0%, 
            rgba(255,255,255,0.08) 100%);
        transform: translateY(-2px);
    }
    
    .search-icon {
        position: absolute;
        right: 25px;
        top: 50%;
        transform: translateY(-50%);
        color: #6366f1;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        filter: drop-shadow(0 2px 4px rgba(99,102,241,0.4));
    }
    
    .search-icon:hover {
        color: #8b5cf6;
        transform: translateY(-50%) scale(1.15) rotate(15deg);
        filter: drop-shadow(0 4px 8px rgba(139,92,246,0.6));
    }

    /* Chatbot section styles */
    .chatbot-section {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.9) 0%, 
            rgba(15, 23, 42, 0.8) 50%, 
            rgba(30, 41, 59, 0.7) 100%);
        border-radius: 28px;
        padding: 45px;
        margin: 40px 0;
        box-shadow: 
            0 25px 80px rgba(0,0,0,0.5), 
            0 12px 40px rgba(99,102,241,0.2),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(30px);
    }

    .chatbot-input-container {
        display: flex;
        gap: 15px;
        align-items: center;
        margin-top: 20px;
    }

    .chatbot-input {
        flex: 1;
        padding: 20px 25px;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,255,255,0.05) 100%);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        color: white;
        font-size: 16px;
        font-weight: 500;
        backdrop-filter: blur(30px);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            inset 0 2px 10px rgba(0,0,0,0.1),
            0 4px 20px rgba(0,0,0,0.1);
    }

    .chatbot-input::placeholder {
        color: rgba(255,255,255,0.7);
        font-style: italic;
    }

    .chatbot-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 
            0 0 0 6px rgba(99, 102, 241, 0.15), 
            0 12px 40px rgba(99, 102, 241, 0.3),
            inset 0 2px 10px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.15) 0%, 
            rgba(255,255,255,0.08) 100%);
    }

    .send-btn {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 20px 25px;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 
            0 8px 24px rgba(99, 102, 241, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
        min-width: 70px;
    }

    .send-btn:hover {
        transform: scale(1.05);
        box-shadow: 
            0 12px 32px rgba(99, 102, 241, 0.5),
            inset 0 1px 0 rgba(255,255,255,0.2);
    }
    
    /* Enhanced feature highlight with animated border */
    .feature-highlight {
        background: linear-gradient(135deg, 
            rgba(220, 38, 38, 0.95) 0%, 
            rgba(234, 88, 12, 0.9) 100%);
        color: white;
        padding: 45px;
        margin: 45px 0;
        border-radius: 28px;
        box-shadow: 
            0 25px 80px rgba(220, 38, 38, 0.4), 
            0 12px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    
    .feature-highlight::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #ff9ff3, #54a0ff);
        border-radius: 30px;
        z-index: -1;
        animation: borderRotate 3s linear infinite;
        opacity: 0.7;
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Enhanced apps section */
    .apps-section {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.9) 0%, 
            rgba(15, 23, 42, 0.8) 100%);
        border-radius: 28px;
        padding: 45px;
        margin: 45px 0;
        box-shadow: 
            0 25px 80px rgba(0,0,0,0.5), 
            0 12px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        backdrop-filter: blur(30px);
    }
    
    .apps-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 30px;
        padding: 35px 0;
        margin: 30px 0;
    }
    
    /* Enhanced app cards with micro-interactions */
    .app-card {
        background: linear-gradient(135deg, 
            rgba(51, 65, 85, 0.8) 0%, 
            rgba(30, 41, 59, 0.6) 100%);
        border-radius: 24px;
        padding: 40px 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid rgba(255,255,255,0.1);
        color: white;
        backdrop-filter: blur(30px);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
    }
    
    .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -150%;
        width: 150%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.15), 
            transparent);
        transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1;
    }
    
    .app-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
        z-index: 0;
    }
    
    .app-card:hover::before {
        left: 150%;
    }
    
    .app-card:hover::after {
        opacity: 1;
    }
    
    .app-card:hover {
        transform: translateY(-15px) scale(1.05);
        border-color: rgba(99,102,241,0.8);
        box-shadow: 
            0 30px 80px rgba(99, 102, 241, 0.5), 
            0 15px 50px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
        background: linear-gradient(135deg, 
            rgba(55, 48, 163, 0.8) 0%, 
            rgba(30, 27, 75, 0.6) 100%);
    }
    
    .app-icon {
        font-size: 3.5rem;
        display: block;
        margin-bottom: 20px;
        filter: drop-shadow(0 6px 12px rgba(0,0,0,0.4));
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 2;
    }
    
    .app-card:hover .app-icon {
        transform: scale(1.2) rotateY(15deg);
        filter: drop-shadow(0 8px 16px rgba(99,102,241,0.4));
    }
    
    .app-name {
        font-size: 1.2rem;
        font-weight: 700;
        text-shadow: 0 2px 6px rgba(0,0,0,0.5);
        position: relative;
        z-index: 2;
    }
    
    /* Enhanced notifications with animated icons */
    .notifications-section {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.9) 0%, 
            rgba(15, 23, 42, 0.8) 100%);
        border-radius: 28px;
        padding: 45px;
        margin: 45px 0;
        box-shadow: 
            0 25px 80px rgba(0,0,0,0.5), 
            0 12px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(30px);
    }
    
    .notification-card {
        background: linear-gradient(135deg, 
            rgba(55, 65, 81, 0.9) 0%, 
            rgba(31, 41, 55, 0.8) 100%);
        border-left: 4px solid #6366f1;
        padding: 30px;
        border-radius: 20px;
        margin: 25px 0;
        display: flex;
        align-items: center;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(30px);
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        position: relative;
        overflow: hidden;
    }
    
    .notification-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at var(--x, 50%) var(--y, 50%), rgba(99,102,241,0.1) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .notification-card:hover::before {
        opacity: 1;
    }
    
    .notification-card:hover {
        transform: translateX(20px) translateY(-5px);
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            0 8px 32px rgba(99,102,241,0.2);
        border-color: rgba(255,255,255,0.2);
    }
    
    .notification-card.spam {
        border-left-color: #dc2626;
    }
    
    .notification-card.fake {
        border-left-color: #f59e0b;
    }
    
    .notification-card.alert {
        border-left-color: #8b5cf6;
    }
    
    .notification-icon {
        font-size: 2.2rem;
        margin-right: 30px;
        filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4));
        min-width: 50px;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .notification-content h4 {
        margin: 0 0 12px 0;
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .notification-content p {
        margin: 0;
        color: rgba(255,255,255,0.85);
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Enhanced buttons with gradient borders */
    .action-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin: 50px 0;
    }
    
    .action-btn {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 25px;
        font-size: 1.3rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 12px 40px rgba(99, 102, 241, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .action-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.2), 
            transparent);
        transition: left 0.6s ease;
    }
    
    .action-btn:hover::before {
        left: 100%;
    }
    
    .action-btn:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(99, 102, 241, 0.5),
            0 10px 40px rgba(139, 92, 246, 0.3);
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #db2777);
    }
    
    .back-btn {
        background: linear-gradient(135deg, 
            rgba(55, 65, 81, 0.9) 0%, 
            rgba(31, 41, 55, 0.8) 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 16px 32px;
        margin: 25px 0;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(20px);
    }
    
    .back-btn:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 12px 32px rgba(0,0,0,0.4),
            0 6px 16px rgba(99,102,241,0.2);
        background: linear-gradient(135deg, 
            rgba(75, 85, 99, 0.9) 0%, 
            rgba(55, 65, 81, 0.8) 100%);
    }
    
    /* Enhanced chat container with holographic effect */
    .chat-container {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.95) 0%, 
            rgba(15, 23, 42, 0.9) 100%);
        border-radius: 28px;
        min-height: 70vh;
        padding: 0;
        margin: 40px 0;
        overflow: hidden;
        box-shadow: 
            0 30px 100px rgba(0,0,0,0.6), 
            0 15px 50px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(30px);
        position: relative;
    }
    
    .chat-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(99,102,241,0.1) 0%, transparent 50%),
                    radial-gradient(circle at 70% 80%, rgba(139,92,246,0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .chat-header {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.9) 0%, 
            rgba(139, 92, 246, 0.8) 50%, 
            rgba(236, 72, 153, 0.7) 100%);
        padding: 30px;
        text-align: center;
        color: white;
        font-weight: 700;
        font-size: 1.4rem;
        box-shadow: 
            0 8px 32px rgba(99, 102, 241, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        position: relative;
        z-index: 1;
        backdrop-filter: blur(20px);
    }
    
    .chat-messages {
        flex: 1;
        padding: 35px;
        overflow-y: auto;
        max-height: 500px;
        scrollbar-width: thin;
        scrollbar-color: rgba(99, 102, 241, 0.6) transparent;
        position: relative;
        z-index: 1;
    }
    
    .chat-messages::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.6) 0%, 
            rgba(139, 92, 246, 0.6) 100%);
        border-radius: 4px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.2);
    }
    
    .chat-input-area {
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.08) 0%, 
            rgba(255,255,255,0.05) 100%);
        padding: 30px;
        border-top: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(30px);
        position: relative;
        z-index: 1;
    }
    
    .message {
        margin: 30px 0;
        animation: messageSlide 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .message.user {
        text-align: right;
    }
    
    .message.system {
        text-align: left;
    }
    
    .message-bubble {
        padding: 25px 30px;
        border-radius: 24px;
        display: inline-block;
        max-width: 75%;
        word-wrap: break-word;
        position: relative;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.15);
        backdrop-filter: blur(30px);
        line-height: 1.6;
        font-size: 1.05rem;
    }
    
    .message.user .message-bubble {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.9) 0%, 
            rgba(139, 92, 246, 0.8) 100%);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .message.system .message-bubble {
        background: linear-gradient(135deg, 
            rgba(55, 65, 81, 0.9) 0%, 
            rgba(31, 41, 55, 0.8) 100%);
        color: white;
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .section-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 50px 0 30px 0;
        padding-left: 20px;
        text-shadow: 
            0 2px 8px rgba(0,0,0,0.4),
            0 0 20px rgba(99,102,241,0.3);
        position: relative;
        letter-spacing: 1px;
    }
    
    .section-title::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 6px;
        height: 50px;
        background: linear-gradient(135deg, 
            #6366f1 0%, 
            #8b5cf6 50%, 
            #ec4899 100%);
        border-radius: 3px;
        box-shadow: 0 0 20px rgba(99,102,241,0.5);
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 6px;
        height: 50px;
        background: linear-gradient(135deg, 
            #6366f1 0%, 
            #8b5cf6 50%, 
            #ec4899 100%);
        border-radius: 3px;
        filter: blur(10px);
        opacity: 0.6;
    }
    
    /* Enhanced login container */
    .login-container {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.95) 0%, 
            rgba(15, 23, 42, 0.9) 100%);
        border-radius: 28px;
        padding: 60px;
        margin: 50px auto;
        max-width: 550px;
        box-shadow: 
            0 30px 100px rgba(0,0,0,0.6), 
            0 15px 50px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(30px);
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 50px;
        position: relative;
        z-index: 1;
    }
    
    .login-icon {
        width: 140px;
        height: 140px;
        background: linear-gradient(135deg, 
            #6366f1 0%, 
            #8b5cf6 50%, 
            #ec4899 100%);
        border-radius: 35px;
        margin: 0 auto 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        box-shadow: 
            0 15px 50px rgba(99, 102, 241, 0.5),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.15);
        animation: iconPulse 3s ease-in-out infinite;
    }
    
    @keyframes iconPulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 15px 50px rgba(99, 102, 241, 0.5);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 20px 60px rgba(99, 102, 241, 0.6);
        }
    }
    
    .verified-container {
        text-align: center;
        padding: 100px 40px;
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.95) 0%, 
            rgba(15, 23, 42, 0.9) 100%);
        border-radius: 28px;
        margin: 40px;
        box-shadow: 
            0 30px 100px rgba(0,0,0,0.6), 
            0 15px 50px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(30px);
        position: relative;
        overflow: hidden;
    }
    
    .verified-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(16,185,129,0.1) 0%, transparent 70%);
        animation: verifiedGlow 4s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes verifiedGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .verified-badge {
        width: 180px;
        height: 180px;
        background: linear-gradient(135deg, 
            #10b981 0%, 
            #059669 50%, 
            #047857 100%);
        border-radius: 50%;
        margin: 0 auto 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4.5rem;
        color: white;
        box-shadow: 
            0 15px 50px rgba(16, 185, 129, 0.5),
            inset 0 2px 0 rgba(255,255,255,0.3);
        animation: verifiedPulse 2.5s ease-in-out infinite;
        border: 2px solid rgba(255,255,255,0.25);
        position: relative;
        z-index: 1;
    }
    
    @keyframes verifiedPulse {
        0% {
            transform: scale(1);
            box-shadow: 0 15px 50px rgba(16, 185, 129, 0.5);
        }
        50% {
            transform: scale(1.05);
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.6);
        }
        100% {
            transform: scale(1);
            box-shadow: 15px 50px rgba(16, 185, 129, 0.5);
        }
    }
    
    .analysis-container {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.95) 0%, 
            rgba(15, 23, 42, 0.9) 100%);
        border-radius: 28px;
        padding: 45px;
        margin: 45px 0;
        box-shadow: 
            0 30px 100px rgba(0,0,0,0.6), 
            0 15px 50px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(30px);
    }
    
    .spam-message {
        background: linear-gradient(135deg, 
            rgba(55, 65, 81, 0.9) 0%, 
            rgba(31, 41, 55, 0.8) 100%);
        border-left: 5px solid #dc2626;
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        color: white;
        backdrop-filter: blur(30px);
        box-shadow: 
            0 12px 40px rgba(220, 38, 38, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }
    
    .analysis-result {
        background: linear-gradient(135deg, 
            rgba(127, 29, 29, 0.95) 0%, 
            rgba(153, 27, 27, 0.9) 100%);
        border: 3px solid #dc2626;
        border-radius: 24px;
        padding: 35px;
        margin: 35px 0;
        color: white;
        box-shadow: 
            0 15px 50px rgba(220, 38, 38, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        backdrop-filter: blur(30px);
    }
    
    /* Enhanced Streamlit components */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        padding: 20px 40px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 12px 40px rgba(99, 102, 241, 0.4) !important,
            inset 0 1px 0 rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(30px) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 
            0 20px 60px rgba(99, 102, 241, 0.5) !important,
            0 10px 40px rgba(139, 92, 246, 0.3) !important;
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #db2777) !important;
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,255,255,0.05) 100%) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 20px !important;
        padding: 20px 25px !important;
        backdrop-filter: blur(30px) !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
        font-style: italic !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 
            0 0 0 6px rgba(99, 102, 241, 0.15) !important,
            0 8px 32px rgba(99, 102, 241, 0.2) !important;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.15) 0%, 
            rgba(255,255,255,0.08) 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,255,255,0.05) 100%) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(30px) !important;
        font-weight: 500 !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 20px 25px !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255,255,255,0.7) !important;
        font-style: italic !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 
            0 0 0 6px rgba(99, 102, 241, 0.15) !important,
            0 8px 32px rgba(99, 102, 241, 0.2) !important;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.15) 0%, 
            rgba(255,255,255,0.08) 100%) !important;
    }
    
    /* Enhanced stats cards with glow effects */
    .stat-card {
        background: linear-gradient(135deg, 
            rgba(55, 65, 81, 0.9) 0%, 
            rgba(31, 41, 55, 0.8) 100%);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        color: white;
        margin: 20px 0;
        box-shadow: 
            0 12px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(30px);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            rgba(99,102,241,0.5), 
            rgba(139,92,246,0.5), 
            rgba(236,72,153,0.5));
        border-radius: 26px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            0 8px 32px rgba(99,102,241,0.2);
    }
    
    .stat-card.critical {
        background: linear-gradient(135deg, 
            rgba(220,  europee38, 38, 0.9) 0%, 
            rgba(153, 27, 27, 0.8) 100%);
        box-shadow: 0 12px 40px rgba(220, 38, 38, 0.4);
    }
    
    .stat-card.warning {
        background: linear-gradient(135deg, 
            rgba(245, 158, 11, 0.9) 0%, 
            rgba(217, 119, 6, 0.8) 100%);
        box-shadow: 0 12px 40px rgba(245, 158, 11, 0.4);
    }
    
    .stat-card.success {
        background: linear-gradient(135deg, 
            rgba(16, 185, 129, 0.9) 0%, 
            rgba(5, 150, 105, 0.8) 100%);
        box-shadow: 0 12px 40px rgba(16, 185, 129, 0.4);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 
            0 2px 8px rgba(0,0,0,0.4),
            0 0 20px currentColor;
        font-family: 'Orbitron', monospace;
    }
    
    .stat-label {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 12px 0 0 0;
        opacity: 0.9;
        letter-spacing: 0.5px;
    }
    
    /* Enhanced form styling */
    .form-group {
        margin: 25px 0;
    }
    
    .form-label {
        display: block;
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 12px;
        padding-left: 6px;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Mobile responsiveness with enhanced effects */
    @media (max-width: 768px) {
        .content-wrapper {
            padding: 25px;
        }
        
        .app-header {
            padding: 40px 25px;
        }
        
        .app-header h1 {
            font-size: 3rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .apps-grid {
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 25px;
        }
        
        .action-buttons {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .login-container {
            padding: 40px 25px;
            margin: 25px;
        }
        
        .verified-container {
            padding: 60px 25px;
            margin: 25px;
        }
        
        .verified-badge {
            width: 140px;
            height: 140px;
            font-size: 3.5rem;
        }
        
        .message-bubble {
            max-width: 85%;
            padding: 20px 25px;
        }
        
        .chat-messages {
            padding: 25px;
        }
        
        .chat-input-area {
            padding: 25px;
        }
        
        .disclaimer-section {
            padding: 30px 25px;
        }
        
        .feature-highlight {
            padding: 30px 25px;
        }

        .chatbot-input-container {
            flex-direction: column;
            gap: 15px;
        }

        .send-btn {
            width: 100%;
            padding: 15px 25px;
        }
    }
    
    @media (max-width: 480px) {
        .app-header h1 {
            font-size: 2.5rem;
        }
        
        .app-header p {
            font-size: 1.2rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .stat-number {
            font-size: 2.5rem;
        }
        
        .apps-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .login-container {
            padding: 30px 20px;
        }
        
        .login-icon {
            width: 120px;
            height: 120px;
            font-size: 3rem;
        }
    }
    
    /* Additional particle effects */
    .content-wrapper::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(99,102,241,0.02) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(139,92,246,0.015) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(236,72,153,0.01) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
        animation: particleFloat 30s ease-in-out infinite;
    }
    
    @keyframes particleFloat {
        0%, 100% { 
            transform: translateY(0px) rotate(0deg); 
            opacity: 0.5;
        }
        33% { 
            transform: translateY(-30px) rotate(120deg); 
            opacity: 0.8;
        }
        66% { 
            transform: translateY(15px) rotate(240deg); 
            opacity: 0.6;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_app' not in st.session_state:
    st.session_state.selected_app = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"type": "system", "message": "🛡️ Welcome to SpamX protected chat! Your messages are being scanned for spam and malicious content."},
        {"type": "user", "message": "Hey! How's the new security feature working?"},
        {"type": "system", "message": "🎯 Excellent! SpamX has blocked 3 spam messages today and detected 2 phishing attempts. Your data is safe!"},
        {"type": "user", "message": "That's awesome! I feel much safer now."},
        {"type": "system", "message": "🔒 We're continuously monitoring for threats. Feel free to chat normally - we've got your back!"}
    ]
if 'chatbot_messages' not in st.session_state:
    st.session_state.chatbot_messages = [
        {"type": "system", "message": "🤖 Hello! users test our agent for miss information verification"}
    ]

# Navigation functions
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def navigate_to(page, app=None):
    st.session_state.current_page = page
    if app:
        st.session_state.selected_app = app

def go_back():
    st.session_state.current_page = 'home'
    st.session_state.selected_app = None

# Google Search function
def google_search(query):
    search_results = [
        {
            "title": f"Search results for: {query}",
            "description": "Your search results would appear here with SpamX protection",
            "url": "https://example.com"
        }
    ]
    return search_results

# Disclaimer Section
st.markdown("""
<div class="disclaimer-section">
    <h3>📢 Disclaimer </h3>
    <p><strong>This is our prototype application Since we developed our app as APK.</strong></p>
    <p>We provided this Streamlit version to showcase our prototype.</p>
</div>
""", unsafe_allow_html=True)

# Content wrapper
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Home Page
if st.session_state.current_page == 'home':
    
    # Google Search Section
    st.markdown("""
    <div class="google-search-section">
        <h2 style="color: white; margin: 0 0 25px 0; text-align: center; font-weight: 600;">🔍 Secure Google Search</h2>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin-bottom: 25px; font-size: 1.1rem;">If you browse using this search engine, we have added extension such that it detects the illegal website and closes the tab, so it avoids mislead activities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input("🔍 Search Google with SpamX Protection", placeholder="Enter your search query...", key="google_search")
    
    if search_query:
        if st.button("🔍 Search Securely"):
            st.success(f"🛡️ Searching for: {search_query} with SpamX protection enabled")
            st.info("🔒 All search results will be scanned for malicious links and content")

    # Chatbot Section
    st.markdown("""
    <div class="chatbot-section">
        <h2 style="color: white; margin: 0 0 25px 0; text-align: center; font-weight: 600;">🤖 SpamX Assistant</h2>
        <p style="color: rgba(255,255,255,0.8); text-align: center; margin-bottom: 25px; font-size: 1.1rem;">Ask me anything about spam detection and security</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat container for messages
    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <span>🤖</span>
            <span>SpamX Assistant Chat</span>
            <span>🔒</span>
        </div>
        <div class="chat-messages">
    """, unsafe_allow_html=True)

    # Display chatbot messages
    for msg in st.session_state.get('chatbot_messages', []):
        if msg["type"] == "user":
            st.markdown(f"""
            <div class="message user">
                <div class="message-bubble">
                    <strong>👤 You:</strong><br>
                    {msg["message"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message system">
                <div class="message-bubble">
                    <strong style="color: #6366f1;">🤖 SpamX:</strong><br>
                    {msg["message"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
        </div>
        <div class="chat-input-area">
    """, unsafe_allow_html=True)

    # Chatbot input and send logic
    col1, col2 = st.columns([5, 1])
    with col1:
        chatbot_input = st.text_input("", placeholder="Ask SpamX Assistant anything...", key="chatbot_input", label_visibility="collapsed")
    with col2:
        send_chatbot = st.button("📤", key="send_chatbot", help="Send message", disabled=st.session_state.get('processing_message', False))

    if send_chatbot and chatbot_input and not st.session_state.get('processing_message', False):
        # Set processing flag to prevent multiple submissions
        st.session_state.processing_message = True
        
        try:
            # Add user message
            st.session_state.chatbot_messages.append({"type": "user", "message": chatbot_input})
            
            # Show spinner while processing
            with st.spinner("🤖 SpamX Assistant is processing..."):
                response = run_async(agent_handler(chatbot_input.lower()))
                print(f"streamlit response: {response}")
            
            # Add bot response
            st.session_state.chatbot_messages.append({"type": "system", "message": response})
        except Exception as e:
            print(f"Error processing agent_handler: {e}")
            st.write("Debug info:", f"Error processing agent_handler: {e}")

            st.session_state.chatbot_messages.append({"type": "system", "message": e})
        finally:
            # Reset processing flag
            st.session_state.processing_message = False
        
        # Trigger rerun to update UI
        st.rerun()

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # App selection buttons
    st.markdown('<h2 class="section-title">🤖 Protected Applications with Agent</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    apps_data = [
        ("Telegram", "📱"),
        ("Reddit", "🟠"), 
        ("Discord", "💬"),
        ("Slack", "📋"),
        ("Instagram", "📸")
    ]
    
    for i, (app, icon) in enumerate(apps_data):
        with [col1, col2, col3, col4, col5][i]:
            if st.button(f"{icon} {app}", key=f"app_{app}"):
                navigate_to('login', app)
                st.rerun()
    
    # Notifications Section
    st.markdown('<h2 class="section-title">🔔 Recent Security Alerts</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="notifications-section">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #6366f1; margin-top: 0; font-size: 1.3rem; font-weight: 600;">📅 Today</h3>', unsafe_allow_html=True)
    
    # Today's notifications with enhanced styling
    notifications_today = [
        ("🚨", "Fake News Detected ❌", "Misinformation about disease spread blocked on Reddit", "fake"),
        ("🛡️", "Spam Messages Blocked!", "❌ 5 spam messages intercepted on Telegram", "spam"),
        ("⚠️", "Phishing Alert!", "Suspicious Discord invite link detected and blocked", "alert")
    ]
    
    for icon, title, message, alert_type in notifications_today:
        with st.container():
            col1, col2 = st.columns([1, 9])
            with col1:
                st.markdown(f'<div style="font-size: 2rem; text-align: center; margin-top: 15px;">{icon}</div>', unsafe_allow_html=True)
            with col2:
                border_colors = {"fake": "#f59e0b", "spam": "#dc2626", "alert": "#8b5cf6"}
                st.markdown(f"""
                <div class="notification-card {alert_type}" style="
                    background: linear-gradient(135deg, #374151 0%, #1f2937 100%); 
                    border-left: 4px solid {border_colors.get(alert_type, '#6366f1')}; 
                    padding: 20px; 
                    border-radius: 12px; 
                    margin: 15px 0; 
                    color: white;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
                    border: 1px solid rgba(255,255,255,0.05);
                    transition: all 0.3s ease;">
                    <h4 style="margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 600;">{title}</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.95rem; line-height: 1.4;">{message}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔔 View All Notifications", key="view_notifications"):
            navigate_to('notifications')
            st.rerun()
    with col2:
        if st.button("📊 Analytics", key="analytics_btn"):
            navigate_to('analysis')
            st.rerun()

    # Feature highlight moved to last
    st.markdown("""
    <div class="feature-highlight">
        <h3 style="margin: 0 0 15px 0; font-size: 1.4rem; font-weight: 600;">🎯 "Win a Free iPhone! Click Here Before It's Too Late!"</h3>
        <p style="margin: 0; font-size: 1.1rem; line-height: 1.6;"><strong>⚠️ Classic phishing/spam tactic detected!</strong></p>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; line-height: 1.6;">Our AI-powered system identifies and blocks misleading messages before they reach you. Stay protected with real-time threat detection!</p>
    </div>
    """, unsafe_allow_html=True)

# Login Page
elif st.session_state.current_page == 'login':
    if st.button("← Back", key="back_login", help="Return to home"):
        go_back()
        st
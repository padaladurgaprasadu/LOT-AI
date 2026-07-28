import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.agents.router import ModelRouter

async def test_pillar_4():
    print("=== Testing G-Stack Generative SaaS Engine ===")
    
    project_name = "twitter_clone_saas"
    
    schema_sql = """
CREATE TABLE tweets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""
    
    frontend_code = """
import React, { useState, useEffect } from 'react';
import { supabase } from './supabaseClient';

export default function App() {
    const [tweets, setTweets] = useState([]);
    
    useEffect(() => {
        const fetchTweets = async () => {
            const { data } = await supabase.from('tweets').select('*');
            setTweets(data || []);
        };
        fetchTweets();
    }, []);
    
    return (
        <div className="p-4 bg-gray-900 text-white min-h-screen">
            <h1 className="text-3xl font-bold mb-4">G-Stack Twitter Clone</h1>
            {tweets.map(t => <div key={t.id} className="p-2 border-b border-gray-700">{t.content}</div>)}
        </div>
    );
}
"""

    print("Triggering Router to scaffold G-Stack SaaS...")
    result_json = await ModelRouter.trigger_gstack_build(project_name, schema_sql, frontend_code)
    
    print("\n=== Result ===")
    print(result_json)

if __name__ == "__main__":
    asyncio.run(test_pillar_4())

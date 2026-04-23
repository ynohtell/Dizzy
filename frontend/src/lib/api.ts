import {API_BASE} from '$lib/constants';

export async function createSession(userId: String) {
    const response = await fetch(`${API_BASE}/sessions/create?user_id=${userId}`, {
        method: "POST"
    });

    if (!response.ok){
        const errorDetail = await response.json();
        throw new Error(typeof errorDetail.detail === 'string' 
            ? errorDetail.detail 
            : JSON.stringify(errorDetail.detail));
    }

    return response.json();
}

export async function getRankings(sessionId:string) {
    const response = await fetch(`${API_BASE}/sessions/${sessionId}/ranking`);
    if (!response.ok) {
        throw new Error ("Could not fetch rankings");
    }
}

export async function submitChoice(sessionId: string, winnerId: string) {
    // We assume your Python backend is running at this base URL
    // (e.g., http://localhost:8000)
    const response = await fetch(`/api/sessions/${sessionId}/vote`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            winner_id: winnerId
        })
    });

    if (!response.ok) {
        // If the backend returns a 400 or 500 error
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to submit choice");
    }

    // This will be the dt.Session object returned by your Python advance_round/submit_choice
    return await response.json();
}


export async function getSession(id: string) {
    const response = await fetch(`/api/session/${id}`);
    if (!response.ok) throw new Error("Could not find session");
    return await response.json();
}
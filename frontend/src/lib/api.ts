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
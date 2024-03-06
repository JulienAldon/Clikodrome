import settings from "../settings";

function getSessions(token) {
    return fetch(`${settings.SERVICE_URL}/sessions`, {
        method:'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function getStudents(token) {
    return fetch(`${settings.SERVICE_URL}/students`, {
        method:'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function editStudent(token, student, id) {
    return fetch(`${settings.SERVICE_URL}/student/${id}`, {
        method: 'PUT',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(student)
    }).then((res) => {
        return res.json();
    });
}

function getRemotes(token) {
    return fetch(`${settings.SERVICE_URL}/remotes`, {
        method:'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}


function getSession(token, id) {
    return fetch(`${settings.SERVICE_URL}/session/${id}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function getSessionSignatures(token, id) {
    return fetch(`${settings.SERVICE_URL}/session/${id}/signature`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function validateSession(token, id) {
    return fetch(`${settings.SERVICE_URL}/session/${id}`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
    }).then((res) => {
        return res.json();
    });
}

function modifySession(token, id, student) {
    let stu = {data: student.map((el) => {
        return {
            status: el.status ? el.status : "NULL", 
            begin: el.begin ? el.begin : "NULL",  
            end: el.end ? el.end : "NULL", 
            login: el.login, 
            id: el.id, 
            session_id: el.session_id
        }
    })}
    return fetch(`${settings.SERVICE_URL}/session/${id}`, {
        method: 'PUT',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(stu)
    }).then((res) => {
        return res.json();
    });
}

function removeSession(token, session_id) {
    return fetch(`${settings.SERVICE_URL}/session/${session_id}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
    }).then((res) => {
        return res.json();
    });
}

function createSession(token, sessionIndex, date, city) {
    let b = {sessionIndex: sessionIndex, date: date, city: city}
    return fetch(`${settings.SERVICE_URL}/session/create`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(b)
    }).then((res) => {
        return res.json();
    });
}

function signSession(token, id) {
    return fetch(`${settings.SERVICE_URL}/session/${id}/sign`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function addRemote(token, student) {
    const b = {login: student.login, begin: student.begin, end: student.end}
    return fetch(`${settings.SERVICE_URL}/remote`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(b)
    }).then((res) => {
        return res.json();
    });
}

function removeRemote(token, id) {
    return fetch(`${settings.SERVICE_URL}/remote/${id}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function checkTodaySession(token) {
    return fetch(`${settings.SERVICE_URL}/sessions/status`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function refreshSession(token, session_id, event_session) {
    let data = {'intra_activity_url': event_session};

    return fetch(`${settings.SERVICE_URL}/session/${session_id}/refresh`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function createPromotion(token, name, sign_id, city) {
    let promo = {name: name, sign_id: sign_id, city: city};

    return fetch(`${settings.SERVICE_URL}/promotion`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(promo)
    }).then((res) => {
        return res.json();
    });
}

function getPromotions(token) {
    return fetch(`${settings.SERVICE_URL}/promotion`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function getPromotion(id, token) {
    return fetch(`${settings.SERVICE_URL}/promotion/${id}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function removePromotion(token, id) {
    return fetch(`${settings.SERVICE_URL}/promotion/${id}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function getWeekplans(token) {
    return fetch(`${settings.SERVICE_URL}/weekplan`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function removeWeekplan(token, id) {
    return fetch(`${settings.SERVICE_URL}/weekplan/${id}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

function createWeekplan(token, day, promotion_id) {
    let weekplan = {promotion_id: promotion_id, day: day};

    return fetch(`${settings.SERVICE_URL}/weekplan`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(weekplan)
    }).then((res) => {
        return res.json();
    });
}

function getEdusignGroups(token) {
    return fetch(`${settings.SERVICE_URL}/edusign/promotions`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json();
    });
}

export {
    getSessions,
    getSession,
    getStudents,
    editStudent,
    getRemotes,
    validateSession,
    modifySession,
    createSession,
    signSession,
    addRemote,
    removeSession,
    removeRemote,
    checkTodaySession,
    refreshSession,
    createPromotion,
    getPromotions,
    getPromotion,
    removePromotion,
    getWeekplans,
    removeWeekplan,
    createWeekplan,
    getEdusignGroups,
    getSessionSignatures
}
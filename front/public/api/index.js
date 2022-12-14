import settings from "../settings";

function getSessions(token) {
    return fetch(`${settings.SERVICE_URL}/sessions`, {
        method:'GET',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json()
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
        return res.json()
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
        return res.json()
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
        return {status: el.status ? el.status : "NULL", login: el.login, late: el.late ? el.late : "NULL"}
    })}
    return fetch(`${settings.SERVICE_URL}/session/${id}`, {
        method: 'PUT',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(stu)
    }).then((res) => {
        return res.json()
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
        return res.json()
    });
}

function createSession(token, sessionIndex) {
    let b = {sessionIndex: sessionIndex}
    return fetch(`${settings.SERVICE_URL}/session/create`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        },
        body: JSON.stringify(b)
    }).then((res) => {
        return res.json()
    })
}

function signSession(token, id) {
    return fetch(`${settings.SERVICE_URL}/session/${id}/sign`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json()
    })
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
        return res.json()
    })
}

function removeRemote(token, id) {
    return fetch(`${settings.SERVICE_URL}/remote/${id}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json()
    })
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

function refreshSession(token, session_id) {
    return fetch(`${settings.SERVICE_URL}/session/${session_id}/refresh`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
			"Authorization": "Bearer " + token
        }
    }).then((res) => {
        return res.json()
    })
}

export {
    getSessions,
    getSession,
    getStudents,
    getRemotes,
    validateSession,
    modifySession,
    createSession,
    signSession,
    addRemote,
    removeSession,
    removeRemote,
    checkTodaySession,
    refreshSession
}
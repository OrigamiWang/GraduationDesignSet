import { requestService } from "../utils/request";

export function fetch(u, m, requestBody) {
    return requestService({
        url: u,
        method: m,
        data: requestBody,
    })

}

export function fetch_form_data(u, m, requestBody) {
    return requestService({
        url: u,
        method: m,
        data: requestBody,
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    })

}

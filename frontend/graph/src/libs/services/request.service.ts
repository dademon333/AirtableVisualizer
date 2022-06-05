const cache: {[key: string]: {value: any, createTime: Date}} = {};

/** GET запрос */
export async function getAsync<T>(url: string, params?: {[key: string]: string}): Promise<T> {
    const response = await fetch(url);
    const data = await response.json();
    return data as T;
}

/** GET запрос с кешированием на время, заданное в настройках */
export async function getCachedAsync<T>(url: string, cacheKey: string, params?: {[key: string]: string}): Promise<T> {
    const cacheTime = Number(process.env.REACT_APP_REQUEST_CACHE_TIME_MS);
    const cacheObject = cache[cacheKey];
    if (cacheObject && cacheObject.createTime.getTime() + cacheTime > Date.now()) {
        return cacheObject.value;
    }

    return getAsync(url, params);
}


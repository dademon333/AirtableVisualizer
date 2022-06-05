import { CourseListEndpoint } from "../endpoints";
import ICourseResponse from "../interfaces/response/course-response.interface";
import { getCachedAsync } from "./request.service";

export async function getCourseListAsync(): Promise<ICourseResponse[]> {
    return getCachedAsync(CourseListEndpoint, 'courseList');
}

export async function getCourseListWithConnectionsAsync(): Promise<ICourseResponse[]> {
    return getCachedAsync(CourseListEndpoint, 'courseListWithConnections');
}
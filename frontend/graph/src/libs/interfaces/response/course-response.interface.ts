interface ICourseResponse {
    name: string;
    type: string;
    size: string;
    description?: string;
    study_time?: string;
    id: number;
    is_hidden: boolean;
}

export default ICourseResponse;
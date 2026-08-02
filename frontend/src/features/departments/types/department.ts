export interface Department {
    id: string;
    name: string;
    description: string | null;

    createdAt: string;
    updatedAt: string;
}

export interface CreateDepartmentPayload {
    name: string;
    description?: string;
}
export interface UpdateDepartmentPayload
    extends CreateDepartmentPayload {
    id: string;
}

export interface DepartmentResponse {
    success: boolean;
    departments: Department[];
}
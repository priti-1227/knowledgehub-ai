import { useState } from "react";
import { Upload, Loader2 } from "lucide-react";
import { useDropzone } from "react-dropzone";

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { useDepartments } from "@/features/departments/hooks/useDepartments";
import { useUploadDocument } from "../hooks/useUploadDocument";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
interface Props {
    open: boolean;
    onOpenChange: (open: boolean) => void;
}
export default function UploadDocumentDialog({
    open,
    onOpenChange,
}: Props) {
    const [title, setTitle] = useState("");
    const [departmentId, setDepartmentId] = useState("");
    const [file, setFile] = useState<File | null>(null);

    const uploadMutation = useUploadDocument();
    const { data } = useDepartments();
    const { getRootProps, getInputProps, isDragActive } =
        useDropzone({
            multiple: false,

            accept: {
                "application/pdf": [],
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    [],
                "text/plain": [],
            },

            onDrop(files) {
                setFile(files[0]);
            },
        });
    async function handleUpload() {
        if (!title || !departmentId || !file) return;

        const formData = new FormData();

        formData.append("title", title);
        formData.append("departmentId", departmentId);
        formData.append("file", file);

        uploadMutation.mutate(formData, {
            onSuccess() {
                setTitle("");
                setDepartmentId("");
                setFile(null);

                onOpenChange(false);
            },
        });
    }

    return (
        <Dialog
            open={open}
            onOpenChange={onOpenChange}
        >
            <DialogContent className="max-w-lg">

                <DialogHeader>
                    <DialogTitle>
                        Upload Document
                    </DialogTitle>
                </DialogHeader>

                <div className="space-y-5">

                    <div>

                        <Label>Title</Label>

                        <Input
                            value={title}
                            onChange={(e) =>
                                setTitle(e.target.value)
                            }
                        />

                    </div>

                    <div>

                        <Label>Department</Label>

                        <Select
                            value={departmentId}
                            onValueChange={setDepartmentId}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Select Department" />
                            </SelectTrigger>

                            <SelectContent>
                                {data?.departments.map((department) => (
                                    <SelectItem
                                        key={department.id}
                                        value={department.id}
                                    >
                                        {department.name}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>

                    </div>

                    <div
                        {...getRootProps()}
                        className={`
          border-2
          border-dashed
          rounded-xl
          p-8
          text-center
          cursor-pointer

          ${isDragActive
                                ? "border-indigo-500 bg-indigo-50"
                                : "border-muted"
                            }
        `}
                    >

                        <input {...getInputProps()} />

                        <Upload className="mx-auto h-10 w-10 mb-3" />

                        {file ? (
                            <p>{file.name}</p>
                        ) : (
                            <p>
                                Drag PDF here
                                <br />
                                or click to browse
                            </p>
                        )}

                    </div>

                    <Button
                        className="w-full"
                        onClick={handleUpload}
                        disabled={uploadMutation.isPending}
                    >
                        {uploadMutation.isPending ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Uploading...
                            </>
                        ) : (
                            "Upload"
                        )}
                    </Button>

                </div>

            </DialogContent>
        </Dialog>
    )
}
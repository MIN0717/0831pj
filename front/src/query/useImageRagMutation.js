import { useMutation } from "@tanstack/react-query";

import { searchImage } from "../api/imageRagApi";


export const useImageRagMutation = () => {
    return useMutation({
        mutationFn: searchImage,
    });
};
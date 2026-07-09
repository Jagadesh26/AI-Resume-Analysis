import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";

import {
  UploadSchema,
  type UploadFormData,
} from "@/types";

interface ResumeUploadFormProps {
  onSubmit: (data: UploadFormData) => void;
}

export function ResumeUploadForm({
  onSubmit,
}: ResumeUploadFormProps) {

  const {

    register,

    handleSubmit,

    setValue,

    formState: { errors },

  } = useForm<UploadFormData>({

    resolver: zodResolver(UploadSchema),

    defaultValues: {

      provider: "gemini",

    },

  });

  return (

    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">

      <motion.div

        initial={{ opacity: 0, y: 40 }}

        animate={{ opacity: 1, y: 0 }}

        className="w-full max-w-3xl rounded-3xl border border-gray-700 bg-gray-800 shadow-2xl"

      >

        <div className="p-10">

          <div className="mb-8 text-center">

            <h1 className="text-4xl font-bold text-white">

              AI Resume Analyzer

            </h1>

            <p className="mt-3 text-gray-400">

              Upload your resume and receive an AI powered ATS analysis.

            </p>

          </div>

          <form

            onSubmit={handleSubmit(onSubmit)}

            className="space-y-8"

          >

            {/* Resume */}

            <div>

              <label className="mb-2 block text-sm font-medium text-gray-300">

                Resume

              </label>

              <div className="relative rounded-2xl border-2 border-dashed border-gray-600 bg-gray-900 p-10 hover:border-orange-500 transition">

                <input

                  type="file"

                  accept=".pdf,.doc,.docx"

                  className="absolute inset-0 cursor-pointer opacity-0"

                  onChange={(event) => {

                    const file = event.target.files?.[0];

                    if (file) {

                      setValue("resume", file, {

                        shouldValidate: true,

                      });

                    }

                  }}

                />

                <div className="text-center">

                  <p className="text-lg font-medium text-white">

                    Drag & Drop Resume

                  </p>

                  <p className="mt-2 text-sm text-gray-400">

                    PDF / DOC / DOCX

                  </p>

                </div>

              </div>

              {errors.resume && (

                <p className="mt-2 text-sm text-red-400">

                  {errors.resume.message}

                </p>

              )}

            </div>

            {/* Provider */}

            <div>

              <label className="mb-2 block text-sm font-medium text-gray-300">

                AI Provider

              </label>

              <select

                {...register("provider")}

                className="w-full rounded-xl border border-gray-600 bg-gray-900 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"

              >

                <option value="gemini">

                  Gemini

                </option>

                <option value="groq">

                  Groq

                </option>

                <option value="openrouter">

                  OpenRouter

                </option>

                <option value="openai">

                  OpenAI

                </option>

                <option value="claude">

                  Claude

                </option>

              </select>

            </div>

            {/* Target Role */}

            <div>

              <label className="mb-2 block text-sm font-medium text-gray-300">

                Target Role

              </label>

              <input

                {...register("targetRole")}

                placeholder="Python Backend Developer"

                className="w-full rounded-xl border border-gray-600 bg-gray-900 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"

              />

              {errors.targetRole && (

                <p className="mt-2 text-sm text-red-400">

                  {errors.targetRole.message}

                </p>

              )}

            </div>

            {/* Submit */}

            <button

              type="submit"

              className="w-full rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 py-4 text-lg font-semibold text-white transition hover:scale-[1.02] hover:shadow-xl hover:shadow-orange-500/20"

            >

              Analyze Resume

            </button>

          </form>

        </div>

      </motion.div>

    </div>

  );

}
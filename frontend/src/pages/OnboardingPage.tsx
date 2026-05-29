import { useState } from "react";

import { API_BASE_URL }
  from "../lib/api";

import {
  useChatStore
} from "../store/chatStore";

export default function OnboardingPage() {

  const [birthDate, setBirthDate] =
    useState("");

  const [birthTime, setBirthTime] =
    useState("");

  const [birthPlace, setBirthPlace] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const {
    setSession
  } = useChatStore();

  async function handleSubmit() {

    if (
      !birthDate ||
      !birthTime ||
      !birthPlace
    ) {
      return;
    }

    setLoading(true);

    try {

      const response = await fetch(

        `${API_BASE_URL}/session/init`,

        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({

            birth_date: birthDate,

            birth_time: birthTime,

            birth_place: birthPlace
          })
        }
      );

      const data =
        await response.json();

      setSession(

        data.session_id,

        {
          birth_date: birthDate,

          birth_time: birthTime,

          birth_place: birthPlace
        }
      );

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);
    }
  }

  return (

    <div className="
      min-h-screen
      bg-slate-950
      text-white
      flex
      items-center
      justify-center
      px-6
    ">

      <div className="
        w-full
        max-w-xl
        bg-slate-900
        border
        border-slate-800
        rounded-3xl
        p-10
      ">

        <h1 className="
          text-5xl
          font-bold
        ">
          AstroAgent
        </h1>

        <p className="
          text-slate-400
          mt-4
        ">
          Begin your chart reading.
        </p>

        <div className="
          mt-10
          space-y-6
        ">

          <input
            type="date"

            value={birthDate}

            onChange={(e) =>
              setBirthDate(
                e.target.value
              )
            }

            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-xl
              px-4
              py-3
            "
          />

          <input
            type="time"

            value={birthTime}

            onChange={(e) =>
              setBirthTime(
                e.target.value
              )
            }

            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-xl
              px-4
              py-3
            "
          />

          <input
            placeholder="Birth place"

            value={birthPlace}

            onChange={(e) =>
              setBirthPlace(
                e.target.value
              )
            }

            className="
              w-full
              bg-slate-950
              border
              border-slate-700
              rounded-xl
              px-4
              py-3
            "
          />

          <button
            onClick={handleSubmit}

            disabled={loading}

            className="
              w-full
              bg-indigo-600
              hover:bg-indigo-500
              py-4
              rounded-xl
              font-medium
            "
          >

            {
              loading

                ? "Generating Chart..."

                : "Begin Your Reading"
            }

          </button>

        </div>

      </div>

    </div>
  );
}
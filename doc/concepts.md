# Concepts for WhatsApp Chat Analysis Project

| Object                   | Context                            | Important Information                                                        |
|--------------------------|------------------------------------|-------------------------------------------------------------------------------|
| Message                  | Raw chat text                      | Text content, media links, emojis, punctuation                                 |
| User                     | Participants in chat               | Username, display name, profile picture, message count                         |
| Timestamp                | Message metadata                   | Date, time, timezone                                                           |
| Chat Group               | Collection of messages             | Group name, participants list, group-level settings (e.g., mute status)        |
| Media                    | Non-text message attachments       | Type (image/video/audio), filename, size, download link                        |
| Emoji                    | Expressive elements in messages    | Unicode code, short name, sentiment mapping                                    |
| Reaction                 | Responses to messages              | Emoji used, reacting user, timestamp                                           |
| Word Frequency           | Text analysis                      | Tokenized words, frequency counts, stopword removal                            |
| Sentiment Score          | Message-level sentiment analysis   | Polarity, subjectivity scores                                                  |
| Time Series              | Temporal analysis                  | Message counts over time buckets (hour/day/week)                               |
| Participant Interaction  | Network analysis                   | Who replies to whom, mention graphs                                            |
| Bot Detection            | Quality control                    | Patterns indicating automated messages, regex-based heuristics                  |
| Language Detection       | Preprocessing                      | Detected language code, confidence                                              |
| Named Entity Recognition | Information extraction             | Persons, locations, organizations, extracted from message text                  |
| Topic Modeling           | Thematic analysis                  | Topics per message or per user, topic distribution                              |

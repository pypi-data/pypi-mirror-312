import csv
import logging

import tqdm

from phi.agent import Agent

from parse_me.name_parsing_agent import ParsedName
from parse_me.name_parsing_prompts import INSTRUCTIONS, LANGS, BASIC_PROMPT


def _parse_name(agent: Agent, name: str, background: str = 'none') -> (dict, list):
    res: ParsedName = agent.run(message=INSTRUCTIONS.format(
        name=name, background=background)).content
    return res.name_parts, res.explanations


def _prepare_agent(language_or_culture: str, model_name: str) -> Agent:
    if language_or_culture not in LANGS:
        raise ValueError("Language or culture {} not found in LANGS, the available options are {}"
                         .format(language_or_culture, LANGS))
    # Choose agent provider
    if model_name.startswith("gpt"):
        from phi.model.openai import OpenAIChat
        model = OpenAIChat(id=model_name)
    elif model_name.startswith("claude"):
        from phi.model.anthropic.claude import Claude
        model = Claude(id=model_name)
    else:
        raise ValueError("Model name {} not recognized, the available options are from the gpt and claude families"
                         .format(model_name))

    # Prepare the agent
    prompt = LANGS[language_or_culture]['parts'][1]
    example = LANGS[language_or_culture]['example']
    language = LANGS[language_or_culture]['language']
    json_mode_agent = Agent(
        model=model,
        description=BASIC_PROMPT.format(language=language, name_parts=prompt, example=example),
        response_model=ParsedName,
    )
    return json_mode_agent


def parse_name(name: str, language: str, background_info: str = '', model_name: str = "gpt-4o") -> dict:
    """
    Parse a single name and return a dictionary with the name parts and an explanation.
    :param name: The name to be parsed
    :param language: Language, script, and perhaps culture of the names from the list of supported combinations
    :param background_info: Additional background about the person whose name is parsed
    :param model_name: a valid open AI model name from the open-AI model specification, defaults to gpt-4o
    :return: dictionary containing the name parts and a special element 'explanations' with the explanation provided
    by the AI model for its choices.
    """
    agent = _prepare_agent(language, model_name)
    parts, explanations = _parse_name(agent, name, background_info)
    parts['explanations'] = explanations
    return parts


def parse_tsv(tsv_file: str, column_name: str, language: str, background_column_name: str = None,
              model_name: str = "gpt-4o") -> str:
    """
    This function takes a tab separated (TSV) file and returns a path to a tsv file
    with the same data but with the names parsed into columns one for each name part
    found and explanations at the end
    :param tsv_file: Path to CSV file containing the names
    :param column_name: Name of the column containing the names
    :param language: Language, script, and perhaps culture of the names from the list of supported combinations
    :param background_column_name: the name of the column in the source file containing additional background
    information about the person whose name is to be parsed.
    :param model_name: a valid open AI model name from the open-AI model specifications, defaults to gpt-4o
    :return: the name of the output file with the results
    """
    # test for existence of file
    try:
        with open(tsv_file, 'r', encoding='utf-8') as f:
            pass
    except FileNotFoundError:
        raise FileNotFoundError("File {} not found".format(tsv_file))

    with open(tsv_file, 'r', encoding='utf-8') as f:
        # test for existence of column_name in file
        reader = csv.DictReader(f, delimiter='\t')
        if column_name not in reader.fieldnames:
            raise ValueError("Column {} not found in file {}".format(column_name, tsv_file))

        agent = _prepare_agent(language, model_name=model_name)
        name_parts = LANGS[language]['parts'][0]
        parsed_names = []
        original_fields = list(reader.fieldnames)
        total_rows = sum(1 for _ in reader)
        f.seek(0)
        batch_count = 0
        res_name = tsv_file + '_parsed.tsv'

        with open(res_name, 'w', encoding='utf-8') as out_f:
            writer = csv.DictWriter(out_f, delimiter='\t',
                                    fieldnames=original_fields + name_parts + ['explanations'],
                                    lineterminator='\n')
            writer.writeheader()

        first = True
        for row in tqdm.tqdm(reader, total=total_rows, desc="Processing rows"):
            if first:
                first = False
                continue
            # Add an entry in parsed_names with the original fields as keys and the values from the row
            new_name_row = {}
            for k in original_fields:
                new_name_row[k] = row[k]

            # Parse the name and add the parsed name parts
            name = row[column_name]
            parsed_name, explanations = _parse_name(agent=agent, name=name,
                                                    background=row.get(background_column_name, 'none'))
            #drop all None values
            parsed_name = {k: v for k, v in parsed_name.items() if v is not None}
            for key in parsed_name.keys():
                if key not in name_parts:
                    logging.warning("Key {} not found in name_parts for row {}".format(key, row))
                    if key == "avonymic":
                        if "patronymic" in new_name_row.keys():
                            new_name_row["patronymic"] = new_name_row["patronymic"] + " " + parsed_name[key]
                        else:
                            new_name_row["patronymic"] = parsed_name[key]
                else:
                    try:
                        if key in new_name_row and new_name_row[key] is not None:
                            new_name_row[key] = new_name_row[key] + " " + str(parsed_name[key])
                        else:
                            new_name_row[key] = parsed_name[key]
                    except TypeError as e:
                        logging.warning("Key {} not found in name_parts for row {}".format(key, row))
                        logging.warning("parsed_name: {}".format(parsed_name))
                        logging.warning("new_name_row: {}".format(new_name_row))

            # Add the explanations to the new_name_row
            new_name_row['explanations'] = explanations

            parsed_names.append(new_name_row)
            batch_count += 1

            # Write to file every 10 rows
            if batch_count == 10:
                with open(res_name, 'a', encoding='utf-8') as out_f:
                    writer = csv.DictWriter(out_f, delimiter='\t',
                                            fieldnames=original_fields + name_parts + ['explanations'],
                                            lineterminator='\n')
                    for row in parsed_names:
                        writer.writerow(row)
                parsed_names = []
                batch_count = 0

        # Write any remaining rows to file
        if parsed_names:
            with open(res_name, 'a', encoding='utf-8') as out_f:
                writer = csv.DictWriter(out_f, delimiter='\t',
                                        fieldnames=original_fields + list(name_parts) + ['explanations'],
                                        lineterminator='\n')
                for row in parsed_names:
                    writer.writerow(row)

    return res_name


def get_supported_languages() -> dict:
    """
    :return: dictionary of language keys and their descriptions
    """
    return {key: value['description'] for key, value in LANGS.items()}

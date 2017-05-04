import observation

NEW_LINE = '\n'
NUMBER_MESSAGES = 10000

with open('generated-data.csv', 'w') as output_file:
    for _ in range(NUMBER_MESSAGES):
        obs = observation.Observation()

        for k in obs.oru['components'].keys():
            hl7 = []
            hl7.append(str(obs.msh_time.strftime("%Y%m%d%H%M%S")))
            hl7.append(str(obs.req_time.strftime("%Y%m%d%H%M%S")))
            hl7.append(str(obs.obs_end_time.strftime("%Y%m%d%H%M%S")))
            hl7.append(str(k))
            hl7.append(str(obs.oru['components'][k]['value']))
            hl7.append(str(obs.oru['components'][k]['unit']))
            hl7.append(str(obs.obx_time.strftime("%Y%m%d%H%M%S")))
            hl7.append(str(obs.oru['method']))

            output_file.write(','.join(hl7) + '\n')
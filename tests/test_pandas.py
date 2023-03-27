import numpy as np
import pandas as pd

if __name__ == '__main__':
    df = pd.DataFrame()

    index_pass = ['pass_cmp', 'pass_att', 'pass_cmp_pct', 'pass_yds_gain',
                  'pass_td', 'pass_td_pct', 'pass_int', 'pass_int_pct',
                  'pass_first_down', 'pass_long', 'pass_sack', 'pass_lateral',
                  'pass_yds_loss', 'pass_net_yds_per_att', 'pass_yds_per_game',
                  'pass_yds_per_cmp']
    index_rcv = ['rcv_targets', 'rcv_recep', 'rcv_yds_gain', 'rcv_yds_per_recep',
                 'rcv_td', 'rcv_first_down', 'rcv_long', 'rcv_per_game',
                 'rcv_yds_per_game', 'rcv_catch_pct']
    index_rush = ['rush_att', 'rush_yds', 'rush_td', 'rush_first_down', 'rush_2pm',
                  'rush_2pa', 'rush_long', 'rush_yds_per_att', 'rush_yds_per_game',
                  'rush_per_game']
    index_fmbl = ['fmbl_ff', 'fmbl_fmbl',
                  'fmbl_recov', 'fmbl_recov_yds', 'fmbl_td']
    index_int = ['int_nb', 'int_yds', 'int_td', 'int_long', 'int_def_pass']
    index_tackle = ['tackle_sk', 'tackl_ast', 'tackle_solo', 'tackle_tfl', 'tackle_qbh',
                    'tackle_blk_kick', 'tackle_safety']
    index_ret_kick = ['ret_kick_nb', 'ret_kick_yds', 'ret_kick_td', 'ret_kick_long',
                      'ret_kick_yds_per']
    index_ret_punt = ['ret_punt_nb', 'ret_punt_yds', 'ret_punt_td', 'ret_punt_long',
                      'ret_punt_yds_per']
    index_kick = ['kick_0-19_fga', 'kick_0-19_fgm', 'kick_20-29_fga', 'kick_20-29_fgm',
                  'kick_30-39_fga', 'kick_30-39_fgm', 'kick_40-49_fga', 'kick_40-49_fgm',
                  'kick_50_fga', 'kick_50_fgm', 'kick_long', 'kick_xp_att', 'kick_xp_made',
                  'kick_fgm', 'kick_fga', 'kick_fg_pct', 'kick_ko_nb', 'kick_ko_yds',
                  'kick_ko_oob', 'kick_ko_tb']
    index_punt = ['punt_nb', 'punt_yds', 'punt_yds_ret', 'punt_yds_net', 'punt_long',
                  'punt_tb', 'punt_in20', 'punt_in20_pct', 'punt_blk']

    index_stats = [*index_pass, *index_rcv, *index_rush, *index_fmbl, *index_int,
                   *index_tackle, *index_ret_kick, *index_ret_punt, *index_kick,
                   *index_punt]
    s1 = pd.Series(0, dtype=object, index=index_stats)
    df["s1"] = s1
    s2 = pd.Series(0, dtype=object, index=index_stats)
    df["s2"] = s2

    print(df)
